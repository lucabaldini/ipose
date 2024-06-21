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

"""Command-line options.
"""

import typing

from ipose import IPOSE_DATA


_OPTION_DICT = {
    # Face detection: opencv setings.
    'scale-factor': dict(type=float, default=1.1,
        help='scaleFactor parameter for the opencv detectMultiScale() call, '
             'determining how much the image size is reduced at each image scale'),
    'min-neighbors': dict(type=int, default=2,
        help='minNeighbors parameter for the opencv detectMultiScale() call, '
             'determining how many neighbors each candidate rectangle should '
             'have to retain it'),
    'min-size': dict(type=float, default=0.175,
        help='minimum rectangle size as a fraction of the effective size of the '
            'original image'),
    # Face cropping: basic appearance.
    'horizontal-padding': dict(type=float, default=0.4,
        help='fractional padding in the horizontal direction for the best rectangle '
             'identified by the face-recognition step'),
    'top-scale-factor': dict(type=float, default=1.25,
        help='scale factor for the top padding, relative to the horizontal padding '
             '(the padding on the bottom will be adjusted to keep the final image square)'),
    'output-size': dict(type=int, default=100,
        help='size of the output (square) image in pixels'),
    'circular-mask': dict(action='store_true', default=False,
        help='if set, a circular mask will be applied in the output image'),
    # Mass processing output options.
    'output-folder': dict(type=str, default=IPOSE_DATA,
        help='path to the folder for the output files'),
    'suffix': dict(type=str, default=None,
        help='optional suffix for the output files'),
    'interactive': dict(action='store_true', default=False,
        help='run in interactive mode')
}



def default_option_value(key: str) -> typing.Any:
    """Return the default value for a given option.

    Parameters
    ----------
    key
        The optional argument name without the leading `--`.

    Returns
    -------
    typing.Any
        The default value for a given optional argument.
    """
    return _OPTION_DICT[key]['default']


def default_option_dict() -> dict:
    """
    """
    return {key: value.default for key, value in _OPTION_DICT.items()}
