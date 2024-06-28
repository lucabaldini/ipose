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

"""Global configuration facilities.
"""


class Configuration(dict):

    _FIELDS = {
        'gui.stylesheet': None,
        'gui.debug': False,
        'gui.header.logo_size': (100, 100),
        'gui.banner.pic_size': (100, 100),
        'gui.poster.width': 1060,
        'gui.footer.height': 25
    }

    """Configuration class.
    """

    def __init__(self) -> None:
        """
        """
        super().__init__(self)
        self.update(**self._FIELDS)



_IPOSE_CONFIG = Configuration()


def get(key: str):
    """
    """
    return _IPOSE_CONFIG[key]


def set(key: str, value) -> None:
    """
    """
    if not key in _IPOSE_CONFIG:
        raise RuntimeError(f'Unrecognized configuration key {key}')
    _IPOSE_CONFIG[key] = value


def update(file_path: str):
    """
    """
    pass
