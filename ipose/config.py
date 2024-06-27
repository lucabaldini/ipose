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
        'gui.debug': False,
        'gui.header.height': 100,
        'gui.header.title_size': 20,
        'gui.header.subtitle_size': 18,
        'gui.banner.pic_size': (100, 100),
        'gui.footer.message_size': 10
    }

    """Configuration class.
    """

    def __init__(self) -> None:
        """
        """
        super().__init__(self)
        self.update(**self._FIELDS)



if __name__ == '__main__':
    config = Configuration()
    print(config)
