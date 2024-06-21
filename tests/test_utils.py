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

import pathlib

import pytest

from ipose import IPOSE_DATA, IPOSE_TEST_DATA, logger
from ipose.utils import check_input_file


def test_check_input_file():
    """Test the check_input_file() function.
    """
    with pytest.raises(RuntimeError) as info:
        check_input_file('nope')
    logger.info(info)
    with pytest.raises(RuntimeError) as info:
        check_input_file(pathlib.Path('nope'))
    logger.info(info)
    with pytest.raises(RuntimeError) as info:
        check_input_file(IPOSE_DATA)
    logger.info(info)
    with pytest.raises(RuntimeError) as info:
        check_input_file(f'{IPOSE_DATA}')
    logger.info(info)
    file_path = IPOSE_TEST_DATA / 'mona_lisa.webp'
    check_input_file(file_path)
    check_input_file(f'{file_path}')
    check_input_file(file_path, '.webp')
    check_input_file(f'{file_path}', '.webp')
    check_input_file(file_path, '.webp', '.png')
    check_input_file(f'{file_path}', '.webp', '.png')
    check_input_file(file_path, '.WEBP')
    check_input_file(f'{file_path}', '.WEBP')
    with pytest.raises(RuntimeError) as info:
        check_input_file(file_path, '.pdf')
    logger.info(info)
    with pytest.raises(RuntimeError) as info:
        check_input_file(f'{file_path}', '.pdf')
    logger.info(info)
