# -*- coding: utf-8 -*-
#
# Copyright © 2014 René Samselnig
#
# This file is part of Database Navigator.
#
# Database Navigator is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Database Navigator is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Database Navigator.  If not, see <http://www.gnu.org/licenses/>.
#


def stat_activity_query(version):
    if version[0] == 9 and version[1] >= 2:
        from .v92 import STAT_ACTIVITY
        return STAT_ACTIVITY
    elif version[:2] == (9, 1):
        from .v91 import STAT_ACTIVITY
        return STAT_ACTIVITY

    raise Exception('Server version {} not supported'.format(version))
