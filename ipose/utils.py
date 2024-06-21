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

"""General utilities.
"""

import pathlib


def check_input_file(file_path: str | pathlib.Path, *extensions: str) -> None:
    """Run some basic checks on a generic input file.

    This raise a RuntimeError whenever there is a problem with the input file
    (e.g., it does not exist, it is not a file or it has the wrong extension).

    Parameters
    ----------
    file_path
        Path to the input file.

    extensions:
        Optional file extensions.
    """
    if not isinstance(file_path, pathlib.Path):
        file_path = pathlib.Path(file_path)
    if not file_path.exists():
        raise RuntimeError(f'Could not find file {file_path}')
    if not file_path.is_file():
        raise RuntimeError(f'{file_path} is not a regular file')
    suffix = file_path.suffix
    extensions = [extension.lower() for extension in extensions]
    if len(extensions) and suffix not in extensions:
        raise RuntimeError(f'Unexpected file extension {suffix}')
