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

import pytest

from ipose import IPOSE_DATA, logger
from ipose.opts import default_value, default_kwargs


def test_default_values():
    """Test the machinery for default values.
    """
    assert default_value('interactive') == False
    assert default_value('overwrite') == False
    assert default_value('output-folder') == IPOSE_DATA
    with pytest.raises(KeyError) as info:
        value = default_value('ops')
    logger.info(info)


def test_default_kwargs():
    """Test the default kwargs.
    """
    logger.info(default_kwargs())
    assert default_kwargs('output-folder') == \
        {'output-folder': default_value('output-folder')}
    assert default_kwargs('interactive', 'overwrite') == \
        dict(interactive=False, overwrite=False)
