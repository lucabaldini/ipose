# Copyright (C) 2024 the ipose team.
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
# along with this program.  If not, see <https://www.gnu.org/licenses/>.


from ipose import logger
from ipose.raster import Rectangle


def test_rectangle_base(x0=400, y0=200, side=100):
    """Basic tests for the rectangle class.
    """
    # Create a random rectangle.
    rect = Rectangle(x0, y0, side, side)
    logger.info(rect)
    # Is a given rectangle equal to itself?
    assert rect == rect.copy()
