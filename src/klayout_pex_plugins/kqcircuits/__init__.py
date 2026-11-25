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

"""Registration for the forthcoming KQCircuits PEX25D scene exporter."""

from .exporter import KQCircuitsSceneExporter


def create_exporter() -> KQCircuitsSceneExporter:
    """Construct the exporter without importing KQCircuits or solver libraries."""
    return KQCircuitsSceneExporter()


__all__ = ['KQCircuitsSceneExporter', 'create_exporter']
