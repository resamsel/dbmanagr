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
from dbnav.model import column


class ColumnTestCase(DbTestCase):
    def test_repr(self):
        """Tests the Column.__repr__ method"""

        con = DbTestCase.connection
        user = con.table('user')
        col = user.column('id')

        self.assertEqual('user.id', repr(col))

    def test_as_json(self):
        """Tests the Column.as_json method"""

        con = DbTestCase.connection
        user = con.table('user')
        col = user.column('id')

        self.assertEqual(
            {
                '__cls__': "<class 'dbnav.model.column.Column'>",
                'name': 'id',
                'table': 'user',
                'type': 'INTEGER',
                'uri': u'dbnav-c.sqlite/user?id'
            },
            col.as_json()
        )

    def test_create_column(self):
        """Tests the column.create_column function"""

        con = DbTestCase.connection
        user = con.table('user')
        col = user.column('id')

        self.assertEqual('id', column.create_column(user, col.name).name)
