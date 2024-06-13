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
    """

    x0: int
    y0: int
    width: int
    height: int

    def area(self) -> int:
        """Return the area of the rectangle.
        """
        return self.width * self.height

    def bounding_box(self):
        """
        """
        return (self.x0, self.y0, self.x0 + self.width, self.y0 + self.width)

    def center(self):
        """
        """
        pass

    def average_side(self):
        """
        """
        pass

    def __lt__(self, other):
        """
        """
        return self.area() < other.area()



def detect_faces(file_path: str, scale_factor: float = 1.1, min_neighbors: int = 5,
    min_fractional_size: float = 0.15) -> list[Rectangle]:
    """Minimal wrapper around the standard opencv face recognition, see, e.g,
    https://www.datacamp.com/tutorial/face-detection-python-opencv

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
        This is converted internally to...

    Returns
    -------
    """
    classifier = cv2.CascadeClassifier(f'{_DEFAULT_FACE_DETECTION_MODEL_PATH}')
    logger.info(f'Running face detection on {file_path}...')
    img = cv2.imread(f'{file_path}')
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    height, width = img.shape
    min_size = round(width * min_fractional_size), round(height * min_fractional_size)
    faces = classifier.detectMultiScale(img, scaleFactor=scale_factor,
        minNeighbors=min_neighbors, minSize=min_size)
    faces = [Rectangle(*face) for face in faces]
    faces.sort()
    return faces




if __name__ == '__main__':
    #file_path = IPOSE_TEST_DATA / 'mona_lisa.webp'
    file_path = IPOSE_TEST_DATA / 'cs_women.webp'
    rects = detect_faces(file_path, min_fractional_size=0.025)
    print(rects)
    with Image.open(file_path) as image:
        draw = ImageDraw.Draw(image)
        for rect in rects:
            draw.rectangle(rect.bounding_box(), outline='white', width=3)
        image.show()
