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

_OPTION_DICT = {
    '--scale-factor': dict(type=float, default=1.1,
        help='scaleFactor parameter for the opencv detectMultiScale() call, '
             'determining how much the image size is reduced at each image scale'),
    '--min-neighbors': dict(type=int, default=2,
        help='minNeighbors parameter for the opencv detectMultiScale() call, '
             'determining how many neighbors each candidate rectangle should '
             'have to retain it'),
    '--min-size': dict(type=float, default=0.175,
        help='minimum rectangle size as a fraction of the effective size of the '
            'original image'),

    '--horizontal-padding': dict(type=float, default=0.4,
        help='fractional padding in the horizontal direction for the best rectangle '
             'identified by the face-recognition step'),
    '--top-scale-factor': dict(type=float, default=1.25,
        help='scale factor for the top padding, relative to the horizontal padding '
             '(the padding on the bottom will be adjusted to keep the final image square)'),
    '--output-size': dict(type=int, default=100,
        help='size of the output (square) image in pixels'),
    '--circular-mask': dict(action='store_true', default=False,
        help='if set, a circular mask will be applied in the output image'),

    '--output-folder': dict(type=str, default=IPOSE_DATA,
        help='path to the folder for the output files'),
    '--suffix': dict(type=str, default=None,
        help='optional suffix for the output files'),
    '--interactive': dict(action='store_true', default=False,
        help='run in interactive mode')
}



def default_value(key: str):
    """
    """
    return _OPTION_DICT[key]['default']



class _Formatter(argparse.RawDescriptionHelpFormatter, argparse.ArgumentDefaultsHelpFormatter):

    """Do nothing class combining our favorite formatting for the
    command-line options, i.e., the newlines in the descriptions are
    preserved and, at the same time, the argument defaults are printed
    out when the --help options is passed.

    The inspiration for this is coming from one of the comments in
    https://stackoverflow.com/questions/3853722
    """



class MainArgumentParser(argparse.ArgumentParser):

    """
    """

    _DESCRIPTION = None
    _EPILOG = None
    _FORMATTER_CLASS = _Formatter
    _OPTS_FACE_DETECTION = ('--scale-factor', '--min-neighbors', '--min-size')
    _OPTS_APPEARANCE = ('--horizontal-padding', '--top-scale-factor', '--output-size', '--circular-mask')
    _OPTS_OUTPUT = ('--output-folder', '--suffix', '--interactive')

    def __init__(self) -> None:
        """Overloaded method.
        """
        super().__init__(description=self._DESCRIPTION, epilog=self._EPILOG,
            formatter_class=self._FORMATTER_CLASS)
        self._add_group('face detection', *self._OPTS_FACE_DETECTION)
        self._add_group('appearance', *self._OPTS_APPEARANCE)
        self._add_group('output', *self._OPTS_OUTPUT)

    @staticmethod
    def _add_arguments_from_dict(parser, *keys: str) -> None:
        """
        """
        for key in keys:
            parser.add_argument(key, **_OPTION_DICT[key])

    def _add_group(self, name: str, *keys: str):
        """
        """
        group = self.add_argument_group(name)
        self._add_arguments_from_dict(group, *keys)
        return group



if __name__ == '__main__':
    parser = MainArgumentParser()
    parser.parse_args()
