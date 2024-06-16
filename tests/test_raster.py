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



from ipose import logger, IPOSE_TEST_DATA, IPOSE_DATA
from ipose.raster import Rectangle, open_image, run_face_recognition, crop_to_face



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

def test_open_image():
    """Test the open_image() function in all its flavors.
    """
    file_path = IPOSE_TEST_DATA / 'mona_lisa.webp'
    image = open_image(file_path)
    image = open_image(str(file_path))

def test_face_recognition():
    """Test the face-detecttion algorithm.
    """
    file_path = IPOSE_TEST_DATA / 'mona_lisa.webp'
    rects = run_face_recognition(file_path, min_neighbors=2, min_fractional_size=0.15)

def test_crop_to_face(interactive=False):
    """Test the actual face crop.
    """
    crop_to_face(IPOSE_TEST_DATA / 'mona_lisa.png', interactive=interactive)
    crop_to_face(IPOSE_TEST_DATA / 'mona_lisa_skinny.png', interactive=interactive)
    crop_to_face(IPOSE_TEST_DATA / 'mona_lisa_fat.png', interactive=interactive)



if __name__ == '__main__':
    test_crop_to_face(interactive=True)
