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


"""Various facilities to operate on raster images.
"""

import dataclasses
import pathlib

import cv2
from matplotlib import pyplot as plt
import matplotlib.patches
import numpy as np
from PIL import Image, ImageDraw

from ipose import logger
from ipose import IPOSE_TEST_DATA

_DEFAULT_FACE_DETECTION_MODEL_PATH = pathlib.Path(cv2.data.haarcascades) / 'haarcascade_frontalface_default.xml'


@dataclasses.dataclass
class Rectangle:

    """Small container class representing a rectangle.

    Parameters
    ----------
    x0
        The x coordinate of the upper-left corner of the rectangle.

    y0
        The y coordinate of the upper-left corner of the rectangle.

    width
        The width of the rectangle.

    height
        The height of the rectangle.
    """

    x0: int
    y0: int
    width: int
    height: int

    def area(self) -> int:
        """Return the area of the rectangle.

        Returns
        -------
        int
            The area of the rectangle.
        """
        return self.width * self.height

    def bounding_box(self) -> tuple[int, int, int, int]:
        """Return the bounding box corresponding to the ractangle, in the form
        of the four-element tuple (xmin, ymin, xmax, ymax).

        Returns
        -------
        tuple[int, int, int, int]
            The four-element tuple corresponding to the rectangle bounding box.
        """
        return (self.x0, self.y0, self.x0 + self.width, self.y0 + self.width)

    def center(self) -> tuple[int, int]:
        """Returns the (rounded) coordinates of the center of the rectangle.

        Returns
        -------
        tuple[int, int]
            The coordinates of the center of the rectangle.
        """
        return (self.x0 + self.width / 2, self.y0 + self.height / 2)

    @staticmethod
    def rounded_geometric_mean(*values: float, scale: float = None) -> int:
        """Return the geometric mean of the input parameters, rounded to the
        nearest integer.

        Parameters
        ----------
        values
            The values to be averaged.

        scale
            Optional multiplicative scale factor, to be applied before the geometric
            average is computed.

        Returns
        -------
        int
            The (rounded) geometric mean of the input data.
        """
        if scale is not None:
            values = [value * scale for value in values]
        return round(np.prod(values)**(1. / len(values)))

    def equivalent_square_side(self) -> int:
        """Return the side of the equivalent square, rounded to the nearest integer
        (which is basically the geometric mean of the rectangle width and height).

        Returns
        -------
        int
            The (rounded) side of the square with the same area as the rectangle.
        """
        return self.rounded_geometric_mean(self.width, self.height)

    def __lt__(self, other):
        """Comparison operator---this is such that :class:`Ractangle` instances
        get sorted by area by default.
        """
        return self.area() < other.area()



def run_face_recognition(file_path: pathlib.Path | str, scale_factor: float = 1.1,
    min_neighbors: int = 5, min_fractional_size: float = 0.15) -> list[Rectangle]:
    """Minimal wrapper around the standard opencv face recognition, see, e.g,
    https://www.datacamp.com/tutorial/face-detection-python-opencv

    Internally this is creating a ``cv2.CascadeClassifier`` object based on a suitable
    model file for face recognition, and running a ``detectMultiScale`` call with
    the proper parameters. The output rectangles containing the candidate faces,
    which are returned by opencv as simple (x, y, width, height) tuples, are
    converted into :class:`Rectangle` objects, and the list of rectangle is sorted
    according to the corresponding area from the smallest to the largest to help
    with the selection process downstream.

    Parameters
    ----------
    file_path
        The path to input image file.

    scale_factor
        Parameter specifying how much the image size is reduced at each image scale
        (passed along verbatim as ``scaleFactor`` to the ``detectMultiScale`` call).

    min_neighbors
        Parameter specifying how many neighbors each candidate rectangle should have
        to retain it (passed along verbatim as ``minNeighbors`` to the ``detectMultiScale``
        call).

    min_fractional_size
        Minimum possible fractional object size. Objects smaller than that are ignored.
        This is converted internally to an actual size in pixels, corresponding
        to a square whose side is the geometric mean of the original width and height,
        multiplied by the parameter value.

    Returns
    -------
    list[Rectangle]
        The list of :class:`Rectangle` objects containing the face candidates.
    """
    # Create a CascadeClassifier object with the proper model file (and the file
    # path must be a string, not a Path, here).
    classifier = cv2.CascadeClassifier(f'{_DEFAULT_FACE_DETECTION_MODEL_PATH}')
    logger.info(f'Running face detection on {file_path}...')
    image = cv2.imread(f'{file_path}')
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # Calculate the minimum size of the output rectangle as that of a square whose
    # side is the geometric mean of the original width and height, multiplied by
    # the min_fractional_size input parameter.
    side = Rectangle.rounded_geometric_mean(*image.shape, scale=min_fractional_size)
    min_size = (side, side)
    logger.debug(f'Minimum rectangle size set to {min_size}.')
    # Run the actual face-detection code.
    candidates = classifier.detectMultiScale(image, scaleFactor=scale_factor,
        minNeighbors=min_neighbors, minSize=min_size)
    # Convert the output to a list of Rectangle objects, and sort by area.
    logger.info(f'Done, {len(candidates)} candidate face(s) found.')
    candidates = [Rectangle(*candidate) for candidate in candidates]
    candidates.sort()
    for i, candidate in enumerate(candidates):
        logger.debug(f'Candidate {i + 1}: {candidate}')
    return candidates




if __name__ == '__main__':
    #file_path = IPOSE_TEST_DATA / 'mona_lisa.webp'
    file_path = IPOSE_TEST_DATA / 'cs_women.webp'
    rects = run_face_recognition(file_path, min_neighbors=2, min_fractional_size=0.02)
    with Image.open(file_path) as image:
        draw = ImageDraw.Draw(image)
        for rect in rects:
            draw.rectangle(rect.bounding_box(), outline='white', width=2)
        image.show()
