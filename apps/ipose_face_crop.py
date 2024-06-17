#!/usr/bin/env python3
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


import argparse

from ipose import IPOSE_DATA
from ipose.pipeline import ipose_face_crop


__description__ = \
"""Crop an image file, or a series of image files, selecting a square region of
the image containing the best close-up face picture within, leveraging opencv for
the face-detection step."""


parser = argparse.ArgumentParser(description=__description__)
parser.add_argument('files', nargs='+')
group = parser.add_argument_group('face recognition')
group.add_argument('--scale-factor', type=float, default=1.1,
    help='scaleFactor parameter for the opencv detectMultiScale() call, '
         'determining how much the image size is reduced at each image scale')
group.add_argument('--min-neighbors', type=int, default=2,
    help='minNeighbors parameter for the opencv detectMultiScale() call, '
         'determining how many neighbors each candidate rectangle should '
         'have to retain it')
group.add_argument('--min-size', type=float, default=0.1,
    help='minimum rectangle size as a fraction of the effective size of the original image')
group = parser.add_argument_group('appearance')
group.add_argument('--horizontal_padding', type=float, default=0.5,
    help='fractional padding in the horizontal direction for the best rectangle '
         'identified by the face-recognition step')
group.add_argument('--top-scale-factor', type=float, default=1.25,
    help='scale factor for the top padding, relative to the horizontal padding '
         '(the padding on the bottom will be adjusted to keep the final image square)')
group.add_argument('--output-size', type=int, default=100,
    help='size of the output (square) image in pixels')
group.add_argument('--circular_mask', action='store_true', default=False,
    help='if set, a circular mask will be applied in the output image')
group = parser.add_argument_group('output')
group.add_argument('--output-folder', type=str, default=IPOSE_DATA,
    help='path to the folder for the output files')
group.add_argument('--suffix', type=str, default=None,
    help='optional suffix for the output files')
group.add_argument('--interactive', action='store_true', default=False,
    help='run in interactive mode')


if __name__ == '__main__':
    kwargs = vars(parser.parse_args())
    for file_path in kwargs.pop('files'):
        ipose_face_crop(file_path, **kwargs)
