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


"""System-wide facilities.
"""

import os
from pathlib import Path
import sys

from loguru import logger

from ipose.version import version as __version__


__PACKAGE_NAME__ = 'ipose'

IPOSE_QT_WRAPPER = 'PyQt6'

# Basic package structure.
IPOSE_ROOT = Path(__file__).parent
IPOSE_BASE = IPOSE_ROOT.parent
IPOSE_DOCS = IPOSE_BASE / 'docs'
IPOSE_EXT = IPOSE_BASE / 'ext'
IPOSE_TESTS = IPOSE_BASE / 'tests'
IPOSE_TEST_DATA = IPOSE_TESTS / 'data'

DEFAULT_LOGURU_FORMAT = '>>> <level>{message}</level>'
DEFAULT_LOGURU_HANDLER = dict(sink=sys.stderr, colorize=True, format=DEFAULT_LOGURU_FORMAT)
logger.configure(handlers=[DEFAULT_LOGURU_HANDLER], levels=None)

# The path to the base folder for the output data defaults to ~/iposedata,
# but can be changed via the $IPOSE_DATA environmental variable.
# Note this folder is created at the first module import if it does not exist.
try:
    IPOSE_DATA = Path(os.environ['IPOSE_DATA'])
except KeyError:
    IPOSE_DATA = Path.home() / 'iposedata'
if not IPOSE_DATA.exists():
    logger.info(f'Creating folder {IPOSE_DATA}...')
    Path.mkdir(IPOSE_DATA, parents=True)
