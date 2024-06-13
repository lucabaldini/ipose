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


def test_rectangle_base():
    """Basic tests for the rectangle class.
    """
    # Create a random rectangle.
    rect = Rectangle(10, 20, 100)
    assert rect.is_square()
    # Is a given rectangle equal to itself?
    assert rect == rect.copy()
    assert rect.bounding_box() == (10, 20, 110, 120)

def test_rectangle_padding():
    """Test the rectangle padding code.
    """
    rect = Rectangle(100, 100, 200)
    assert rect.pad(100, 100, 100, 100) == Rectangle(0, 0, 400, 400)
    assert rect.pad(100, 100) == Rectangle(0, 0, 400, 400)
    assert rect.pad(100) == Rectangle(0, 0, 400, 400)
    assert rect.pad(100, 200) == Rectangle(-100, 0, 600, 400)

def test_rectangle_fitting():
    """Test for rectangle fitting.
    """
    rect = Rectangle(-10, -10, 100, 100)
    assert rect.fit_to_size(400, 200) == Rectangle(0, 0, 100, 100)
    assert rect.fit_to_size(100, 100) == Rectangle(0, 0, 100, 100)
    #print(rect.fit_to_size(80, 100))
