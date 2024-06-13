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
import PIL

from ipose import logger
from ipose import IPOSE_DATA

_DEFAULT_FACE_DETECTION_MODEL = '/usr/share/opencv4/haarcascades/haarcascade_frontalface_default.xml'


@dataclasses.dataclass
class Rectangle:

    """Small container class representing a rectangle as, e.g., returned by the
    opencv pattern detection algorithms.
    """

    x0: int
    y0: int
    width: int
    height: int

    def area(self) -> int:
        """Return the area of the rectangle.
        """
        return self.width * self.height



def face_detection(file_path: str, min_frac_size: float = 0.145):
    """
    """
    classifier = cv2.CascadeClassifier(f'{_DEFAULT_FACE_DETECTION_MODEL}')
    logger.info(f'Running face detection on {file_path}...')
    img = cv2.imread(f'{file_path}')
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    height, width = img.shape
    min_size = round(width * min_frac_size), round(height * min_frac_size)
    faces = classifier.detectMultiScale(img, scaleFactor=1.1, minNeighbors=5, minSize=min_size)
    faces = [Rectangle(*face) for face in faces]
    faces.sort()
    return faces[0]




if __name__ == '__main__':
    file_path = IPOSE_DATA / 'mona_lisa.webp'
    rect = face_detection(file_path)
    print(rect)
    img = np.asarray(PIL.Image.open(file_path))
    plt.imshow(img)
    r = matplotlib.patches.Rectangle((rect.x0, rect.y0), rect.width, rect.height, fill=False, edgecolor='white')
    plt.gca().add_artist(r)
    plt.show()
