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
from dbmanagr.model import table


class TableTestCase(DbTestCase):
    def test_autocomplete_(self):
        """Tests the table.autocomplete_ method"""

        con = DbTestCase.connection
        user = con.table('user')
        id = user.column('id')

        self.assertEqual(
            'dbmanagr-c.sqlite/user/?[BLOB]',
            user.autocomplete_(id, memoryview(b'Blub')))

    def test_subtitle(self):
        """Tests the table.subitle method"""

        con = DbTestCase.connection
        user = con.table('user')

        self.assertEqual(
            'Table',
            user.subtitle())

        user.owner = 'me'
        user.size = '123 kB'

        self.assertEqual(
            'Owner: me (123 kB)',
            user.subtitle())

    def test_table(self):
        """Tests the table.Table class"""

        con = DbTestCase.connection
        user = con.table('user')

        self.assertEqual(
            len(user.columns()),
            len(table.Table(name=user.name, columns=user.columns()).columns())
        )
