#
# --------------------------------------------------------------------------------
# SPDX-FileCopyrightText: 2026 Martin Jan Köhler and Harald Pretl
# Johannes Kepler University, Institute for Integrated Circuits.
#
# This file is part of kpex-plugin-kqcircuits
# (see https://github.com/iic-jku/kpex-plugin-kqcircuits).
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
# SPDX-License-Identifier: GPL-3.0-or-later
# --------------------------------------------------------------------------------
#

"""The unfinished adapter must be discoverable without claiming export success."""

from __future__ import annotations

from importlib import metadata
from pathlib import Path
from types import MappingProxyType
from typing import TYPE_CHECKING

import pytest

if TYPE_CHECKING:
    from conftest import RunPython
    from kpex_protobuf.kpex.pex25d.pex25d_scene_pb2 import PEX25DScene

from kpex import pex25d
from kpex.plugin_api.v1 import ExportError, SceneCapability
from kpex_protobuf.kpex.pex25d import pex25d_capabilities_pb2
from klayout_pex_plugins.kqcircuits import KQCircuitsSceneExporter, create_exporter


def test_registered_factory_is_loadable():
    entry_points = [point for point in metadata.entry_points(group='klayout_pex.exporters.v1')
                    if point.name == 'kqcircuits']
    assert len(entry_points) == 1
    assert entry_points[0].dist.name == 'kpex-plugin-kqcircuits'
    assert isinstance(entry_points[0].load()(), KQCircuitsSceneExporter)
    assert isinstance(create_exporter(), KQCircuitsSceneExporter)


@pytest.mark.parametrize('selector', [
    'kqcircuits', 'kpex-plugin-kqcircuits:kqcircuits',
])
def test_kpex_registry_loads_fresh_exporters(selector: str):
    registry = pex25d.exporter_registry()
    assert registry.get_info(selector).distribution == 'kpex-plugin-kqcircuits'
    first = registry.load(selector)
    assert isinstance(first, KQCircuitsSceneExporter)
    assert registry.load(selector) is not first


@pytest.mark.parametrize('prefix', ['', 'cell_'])
def test_export_reports_unimplemented_without_side_effects(scene: PEX25DScene,
                                                          export_destination: Path,
                                                          prefix: str):
    # Immutable options catch accidental mutation by an adapter.
    before_scene = scene.SerializeToString(deterministic=True)
    options = MappingProxyType({})

    with pytest.raises(NotImplementedError, match='KQCircuits export is not implemented yet'):
        pex25d.export(scene, target='kqcircuits', output_dir_path=str(export_destination),
                      prefix=prefix, options=options)

    assert scene.SerializeToString(deterministic=True) == before_scene
    assert dict(options) == {}


def test_cli_lists_the_installed_plugin(run_python: RunPython):
    result = run_python(['-m', 'kpex.pex25d', 'exporters'])
    assert result.returncode == 0, result.stderr
    assert 'kpex-plugin-kqcircuits:kqcircuits' in result.stdout


def test_cli_reports_not_implemented(scene_path: Path, export_destination: Path, run_python: RunPython):
    result = run_python([
        '-m', 'kpex.pex25d', 'export', str(scene_path),
        '--to', 'kqcircuits', '--out-dir', str(export_destination),
    ])
    output = result.stdout + result.stderr
    assert result.returncode == 3, output
    assert 'KQCircuits export is not implemented yet' in output
    assert 'Traceback' not in output


def test_discovery_and_factory_do_not_load_optional_backends(run_python: RunPython):
    # A fresh interpreter avoids passing only because geometry modules were
    # already imported by another test. Block imports even when installed.
    result = run_python(['-c', """
import importlib.abc
import sys

class NoBackends(importlib.abc.MetaPathFinder):
    def find_spec(self, fullname, path=None, target=None):
        if fullname.split('.')[0] in {
                'klayout', 'pya', 'gmsh', 'kqcircuits', 'kpex_protobuf'}:
            raise AssertionError('Unexpected optional import: ' + fullname)

sys.meta_path.insert(0, NoBackends())
from kpex.pex25d import exporter_registry
registry = exporter_registry()
assert registry.get_info('kqcircuits').name == 'kqcircuits'
assert callable(registry.load('kqcircuits').export)
assert callable(registry.load('fastercap').export)
"""])
    assert result.returncode == 0, result.stderr


def test_namespace_does_not_hide_another_plugin(tmp_path: Path, run_python: RunPython):
    # Install a peer on a distinct import root, just as independently installed
    # distributions can contribute to the same implicit namespace.
    peer_root = tmp_path / 'other distribution'
    peer_package = peer_root / 'klayout_pex_plugins' / 'fixture_peer'
    peer_package.mkdir(parents=True)
    (peer_package / '__init__.py').write_text('IDENTITY = "independent plugin"\n', encoding='utf-8')
    result = run_python(['-c', """
import sys
sys.path.insert(0, sys.argv[1])
import klayout_pex_plugins
from klayout_pex_plugins.kqcircuits import create_exporter
from klayout_pex_plugins.fixture_peer import IDENTITY
assert klayout_pex_plugins.__file__ is None
assert IDENTITY == 'independent plugin'
assert callable(create_exporter().export)
""", str(peer_root)])
    assert result.returncode == 0, result.stderr


@pytest.mark.parametrize('required, floating_collision', [
    pytest.param(SceneCapability.CAPACITANCE_ACCOUNTING, False, id='accounting'),
    pytest.param(SceneCapability.GROUND_CUTOUTS, False, id='ground-cutout'),
    pytest.param(SceneCapability.ELECTRICAL_IDENTITY, False, id='ground-reference-net'),
    pytest.param(SceneCapability.ELECTRICAL_IDENTITY, True, id='floating-net-name-collision'),
])
def test_required_capabilities_are_rejected_without_side_effects(
        scene: PEX25DScene, required: SceneCapability, floating_collision: bool,
        export_destination: Path, tmp_path: Path, run_python: RunPython):
    # Each scene is physically valid. Rejection must identify the missing
    # semantics, rather than a malformed scene or a crash inside the scaffold.
    # Electrical identity covers both a distinct ground net and a collision
    # between a named net and an independent floating conductor.
    match required:
        case SceneCapability.CAPACITANCE_ACCOUNTING:
            scene.required_capabilities.append(
                pex25d_capabilities_pb2.REQUIRED_CAPABILITY_CAPACITANCE_ACCOUNTING)
            scene.capacitance_accounting.excluded_substrate_nets.append('neta')
        case SceneCapability.GROUND_CUTOUTS:
            scene.ground_plane.net = scene.ground_plane.name
            opening = scene.ground_plane.cutouts.add()
            for x, y in [(-1000, -1000), (0, -1000), (0, 0), (-1000, 0)]:
                opening.polygon.outer.points.add(x=x, y=y)
        case SceneCapability.ELECTRICAL_IDENTITY:
            if floating_collision:
                next(conductor for conductor in scene.conductors if conductor.name == 'A').net = 'F'
            else:
                scene.ground_plane.net = 'VSS'
        case _:
            raise NotImplementedError(f'Capability rejection fixture for {required!r}')

    report = pex25d.validate(scene)
    assert report.num_errors == 0, report.diagnostics
    before_scene = scene.SerializeToString(deterministic=True)
    options = MappingProxyType({})
    with pytest.raises(ExportError, match='does not support required scene capabilities') as error:
        pex25d.export(scene, target='kqcircuits', output_dir_path=str(export_destination), options=options)
    assert required.value in str(error.value)
    assert scene.SerializeToString(deterministic=True) == before_scene
    assert dict(options) == {}

    artifact = tmp_path / 'input.pex25d.scene.pb'
    artifact.write_bytes(before_scene)
    result = run_python([
        '-m', 'kpex.pex25d', 'export', str(artifact),
        '--to', 'kqcircuits', '--out-dir', str(export_destination),
    ])
    output = result.stdout + result.stderr
    assert result.returncode == 2, output
    # Rich may insert its source-location column between wrapped message lines.
    assert 'required scene capabilities:' in output, output
    assert required.value in output, output
    assert 'Traceback' not in output, output
    assert artifact.read_bytes() == before_scene
