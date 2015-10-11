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

from tests.testcase import DbTestCase
from dbmanagr.driver.postgresql import version


class VersionTestCase(DbTestCase):
    def test_stat_activity_query(self):
        """Tests the postgresql version stat_activity_query function"""

        self.assertIsNotNone(version.stat_activity_query((9, 2, 0)))
        self.assertIsNotNone(version.stat_activity_query((9, 1, 0)))
        self.assertRaises(
            Exception,
            version.stat_activity_query,
            [[9, 0, 0]]
        )
