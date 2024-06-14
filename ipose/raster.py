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

from __future__ import annotations

import dataclasses
import numbers
import pathlib

import cv2
from matplotlib import pyplot as plt
import matplotlib.patches
import numpy as np
from PIL import Image, ImageDraw

from ipose import logger
from ipose import IPOSE_TEST_DATA


_EXIF_ORIENTATION_TAG = 274
_EXIF_ROTATION_DICT = {3: 180, 6: 270, 8: 90}
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
    height: int = None

    def __post_init__(self) -> None:
        """Post initialization code.
        """
        # By deafult, generate a square.
        if self.height is None:
            self.height = self.width
        # Also, make sure all the members are integers, as we are dealing with
        # pixels in rastered images. Note that we are using numbers.Integral, as
        # opposed to the native Python int, as we want to be able to catch the
        # numpy integral types as well.
        for item in (self.x0, self.y0, self.width, self.height):
            if not isinstance(item, numbers.Integral):
                raise RuntimeError(f'Wrong type for {self}')

    def copy(self) -> Rectangle:
        """Return an identical copy of the rectangle.

        Returns
        -------
        Rectangle
            A new Rectangle object, identical to the original one.
        """
        return Rectangle(self.x0, self.y0, self.width, self.height)

    def is_square(self) -> bool:
        """Return True if the rectangle is square.

        Returns
        -------
        bool
            True if the rectangle is squared.
        """
        return self.width == self.height

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

    def center(self) -> tuple[float, float]:
        """Returns the coordinates of the center of the rectangle.

        Returns
        -------
        tuple[float, float]
            The coordinates of the center of the rectangle.
        """
        return (self.x0 + self.width / 2., self.y0 + self.height / 2.)

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

        Whenever the `fractional` word is used in the context of a rectangle, this
        is the scale constituting the multiplier for the operation at hand.

        Returns
        -------
        int
            The (rounded) side of the square with the same area as the rectangle.
        """
        return self.rounded_geometric_mean(self.width, self.height)

    def pad(self, top: int, right: int = None, bottom: int = None, left: int = None) -> Rectangle:
        """Pad the rectangle according to the input parameters.

        Note that the order of the arguments is designed to make it easy for the
        user to specify a single padding on four sides (passing only one argument)
        different vertical and horizontal paddings (passing two arguments), as well
        as arbitrary configurations.

        Parameters
        ----------
        top
            The top padding in pixels.

        right
            The right padding in pixels.

        bottom
            The bottom padding in pixels.

        left
            The left padding in pixels.

        Returns
        -------
        Rectangle
            A new Rectangle object, properly padded with respect to the original one.
        """
        right = right or top
        bottom = bottom or top
        left = left or right
        return Rectangle(self.x0 - left, self.y0 - top, self.width + right + left,
            self.height + top + bottom)

    def pad_face(self, horizontal_fractional_padding: float = 0.5,
        top_scale_factor: float = 1.25) -> Rectangle:
        """Specialized function for padding a rectangle given by :meth:`run_face_recognition`.

        This is essentially adding a horizontal padding given by the first argument
        and asymmetric top-bottom padding governed by the second. The rationale behind
        this is that opencv tends to crop the hair, and we generally want a padding
        on the top that is slightly larger than that on the bottom.

        Note that this function guarantees that the sum of the horizontal and vertical
        paddings are the same---that is, if we start from a square rectangle, we do
        end up with a square rectangle.

        Parameters
        ----------
        horizontal_fractional_padding
            The horizontal padding, on either side, in units of the equivalent ]
            square side of the rectangle.

        top_scale_factor
            The ratio between the pad on the top and that on the right/left.

        Returns
        -------
        Rectangle
            A new Rectangle object, padded accordingly.
        """
        right = round(horizontal_fractional_padding * self.equivalent_square_side())
        top = round(top_scale_factor * right)
        bottom = 2 * right - top
        return self.pad(top, right, bottom)

    def fit_to_size(self, width: int, height: int) -> Rectangle:
        """Fit a given rectangle to a given image canvas.

        Parameters
        ----------
        width
            The width of the target canvas image in pixels.

        height
            The height of the target canvas image in pixels.

        Returns
        -------
        Rectangle
            A new Rectangle object fitting into the target canvas.
        """
        # Create a verbatim copy of the original rectangle...
        rect = self.copy()
        # ...and work our way to the desired rectangle.
        if rect.width > width:
            rect.width = width
        if rect.height > height:
            rect.height > height
        if self.is_square() and not rect.is_square():
            raise RuntimeError('Final rectangle is not square.')
        if rect.x0 < 0:
            rect.x0 = 0
        if rect.y0 < 0:
            rect.y0 = 0
        return rect

    def __eq__(self, other) -> bool:
        """Overloaded equality operator.
        """
        return self.x0 == other.x0 and self.y0 == other.y0 and \
            self.width == other.width and self.height == other.height

    def __lt__(self, other) -> bool:
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

    Note that this is producing squares (since apparently this is the way the default
    model we are using was trained) that are only big enough to cover the visible
    part of the face, and if you use this to crop a large image to the person face
    it is very likely that you will want to add some padding on the four sides,
    and especially on the top, which empirically seems to be the most overlooked
    part of the face.

    The ``min_neighbors`` parameter has an important effect on the results and
    should be set on a case-by-case basis. The cascade classifier applies a sliding
    window through the image, and initially it will capture a large number of false
    positives. This parameter specifies the number of neighboring rectangles that
    need to be identified for an object to be considered a valid detection: a value
    of 0 is idiotic, and it will likely return an enourmous number of (possibly
    overlapping) rectangles. Small values will yield comparatively more false positives.
    I would say 2 is the absolute minimum one migh consider using, and something
    around 5 is more germane to what is commonly found in tutorials online.

    Parameters
    ----------
    file_path
        The path to input image file.

    scale_factor
        Parameter specifying how much the image size is reduced at each image scale
        (passed along verbatim as ``scaleFactor`` to the ``detectMultiScale`` call).

    min_neighbors
        Parameter specifying how many neighbors each candidate rectangle should
        have to retain it (passed along verbatim as ``minNeighbors`` to the
        ``detectMultiScale`` call).

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


def open_image(source: str | pathlib.Path | Image.Image) -> Image.Image:
    """Open an existing image in read mode.

    This is designed to make the downstream methods interoperable with either
    pre-loaded images or image data on files, in that: if an Image.Image object is
    passed as the first argument, the latter is returned immediately, while if the
    firts argument is a string or a path, the correspoding file is opened in read
    mode and the image within is returned.

    Note the image is automatically rotated is the proper EXIF tag is found.

    Parameters
    ----------
    source
        The source of image data (i.e., an actual image or a path to an image file)

    Returns
    -------
    PIL.Image.Image
        The actual image object.
    """
    if isinstance(source, Image.Image):
        return source
    logger.info(f'Loading image data from {source}...')
    with Image.open(file_path) as image:
        # Parse the original image size and orientation.
        w, h = image.size
        orientation = image.getexif().get(_EXIF_ORIENTATION_TAG, None)
        logger.debug(f'Original size: {w} x {h}, orientation: {orientation}')
    # If the image is rotated, we need to change the orientation.
    rotation = _EXIF_ROTATION_DICT.get(orientation, None)
    if rotation is not None:
        logger.debug(f'Applying a rotation by {rotation} degrees...')
        image = image.rotate(rotation, expand=True)
        w, h = image.size
        logger.debug(f'Rotated size: {w} x {h}')
    return image


def crop_image_to_face():
    """
    """
    pass




if __name__ == '__main__':
    file_path = IPOSE_TEST_DATA / 'mona_lisa.webp'
    #file_path = IPOSE_TEST_DATA / 'cs_women.webp'
    rects = run_face_recognition(file_path, min_neighbors=2, min_fractional_size=0.02)
    image = open_image(file_path)
    draw = ImageDraw.Draw(image)
    for rect in rects:
        print('Original: ', rect)
        draw.rectangle(rect.bounding_box(), outline='white', width=2)
        pad_rect = rect.pad_face()
        print('Padded:', pad_rect)
        pad_rect = pad_rect.fit_to_size(*image.size)
        print('Fitted: ', pad_rect)
        draw.rectangle(pad_rect.bounding_box(), outline='red', width=2)
    image.show()
