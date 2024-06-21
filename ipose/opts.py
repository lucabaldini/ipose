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

import argparse
import typing

from ipose import IPOSE_DATA
import ipose.pipe


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



class _Formatter(argparse.RawDescriptionHelpFormatter, argparse.ArgumentDefaultsHelpFormatter):

    """Do nothing class combining our favorite formatting for the
    command-line options, i.e., the newlines in the descriptions are
    preserved and, at the same time, the argument defaults are printed
    out when the --help options is passed.

    The inspiration for this is coming from one of the comments in
    https://stackoverflow.com/questions/3853722
    """



class MainArgumentParser(argparse.ArgumentParser):

    """Application-wide argument parser.
    """

    _DESCRIPTION = None
    _EPILOG = None
    _FORMATTER_CLASS = _Formatter

    def __init__(self) -> None:
        """Overloaded method.
        """
        super().__init__(description=self._DESCRIPTION, epilog=self._EPILOG,
            formatter_class=self._FORMATTER_CLASS)
        subparsers = self.add_subparsers(required=True, help='sub-command help')
        # See https://stackoverflow.com/questions/8757338/
        subparsers._parser_class = argparse.ArgumentParser
        # Face cropping
        parser_facecrop = subparsers.add_parser('facecrop', help='crop images to face')
        self.add_face_detection_group(parser_facecrop)
        self.add_appearance_group(parser_facecrop)
        self.add_output_group(parser_facecrop)
        self.add_file_list(parser_facecrop)
        parser_facecrop.set_defaults(func=ipose.pipe.face_crop)

        parser_facetile = subparsers.add_parser('facetile', help='tile face images')

    @staticmethod
    def _add_options_from_dict(container: argparse._ActionsContainer, *keys: str) -> None:
        """Add one or more optional arguments to a given container.

        Parameters
        ----------
        container
            The action container, typically the main OptionParser itself or a
            child option group.

        keys
            The name of the optional argument(s) to be added, whose keyword arguments
            must be defined in the `_OPTION_DICT` variable at the top of the module.
        """
        for key in keys:
            container.add_argument(f'--{key}', **_OPTION_DICT[key])

    @staticmethod
    def add_option_group(container: argparse._ActionsContainer, name: str,
        *keys: str) -> argparse._ArgumentGroup:
        """Add a new option group to the parser, based on the `_OPTION_DICT` variable
        at the top of the module.

        Parameters
        ----------
        name
            The name of the option group.

        keys
            The name of the optional argument(s) to be added, whose keyword arguments
            must be defined in the `_OPTION_DICT` variable at the top of the module.

        Returns
        -------
        argparse._ArgumentGroup
            The newly created group.
        """
        group = container.add_argument_group(name)
        MainArgumentParser._add_options_from_dict(group, *keys)
        return group

    @staticmethod
    def add_file_list(container: argparse._ActionsContainer) -> None:
        # pylint: disable=missing-function-docstring
        container.add_argument('file-list', nargs='+',
            help='list of input file(s) to be processed')

    @staticmethod
    def add_face_detection_group(container: argparse._ActionsContainer) -> None:
        # pylint: disable=missing-function-docstring
        keys = ('scale-factor', 'min-neighbors', 'min-size')
        MainArgumentParser.add_option_group(container, 'face detection', *keys)

    @staticmethod
    def add_appearance_group(container: argparse._ActionsContainer) -> None:
        # pylint: disable=missing-function-docstring
        keys = ('horizontal-padding', 'top-scale-factor', 'output-size', 'circular-mask')
        MainArgumentParser.add_option_group(container, 'appearance', *keys)

    @staticmethod
    def add_output_group(container: argparse._ActionsContainer) -> None:
        # pylint: disable=missing-function-docstring
        keys = ('output-folder', 'suffix', 'interactive')
        MainArgumentParser.add_option_group(container, 'output', *keys)

    def run_command(self) -> None:
        """Run the actual command tied to the specific options.
        """
        kwargs = vars(self.parse_args())
        file_list = kwargs.pop('file-list')
        command = kwargs.pop('func')
        for file_path in file_list:
            command(file_path, **kwargs)
