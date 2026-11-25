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

"""Partner implementation boundary for KQCircuits solver-input generation."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, List, Mapping, Optional

if TYPE_CHECKING:
    from kpex_protobuf.kpex.pex25d.pex25d_scene_pb2 import PEX25DScene


class KQCircuitsSceneExporter:
    """Reserved exporter target; scene translation is not implemented yet.

    The eventual implementation writes KQCircuits/Elmer simulation inputs from
    a resolved scene. Running the solver remains a separate operation.
    """

    def export(self,
               scene: PEX25DScene,
               *,
               output_dir_path: str,
               prefix: str = '',
               options: Optional[Mapping[str, Any]] = None) -> List[str]:
        """Report the unfinished adapter without changing inputs or output files.

        NotImplementedError follows plugin API v1 and gives the CLI its
        unsupported-operation exit status. No backend options are supported yet.
        """
        raise NotImplementedError(
            'KQCircuits export is not implemented yet. '
            'kpex-plugin-kqcircuits currently provides the development scaffold, '
            'not a working scene translator.')
