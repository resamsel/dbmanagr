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

from os import path

from tests.testcase import DbTestCase
from dbnav.model import databaseconnection
from tests.mock.sources import DIR as MOCK_DIR
from tests.mock.sources import URI as MOCK_URI


class DatabaseConnectionTestCase(DbTestCase):
    def test_inspector(self):
        """Tests the DatabaseConnection inspector method"""

        con = DbTestCase.connection

        self.assertIsNotNone(con.inspector())

    def test_filter(self):
        """Tests the DatabaseConnection filter method"""

        con = databaseconnection.DatabaseConnection()

        self.assertEquals(
            None,
            con.filter_(None)
        )

        con.close()

    def test_databases(self):
        """Tests the DatabaseConnection databases method"""

        con = databaseconnection.DatabaseConnection()
        con.connect_to(MOCK_URI.format(
            file=path.join(
                MOCK_DIR, '../resources/dbnav.sqlite')))

        self.assertEquals(
            [],
            con.databases()
        )

        con.close()

    def test_connected(self):
        """Tests the DatabaseConnection connected method"""

        con = databaseconnection.DatabaseConnection()
        con.connect_to(MOCK_URI.format(
            file=path.join(
                MOCK_DIR, '../resources/dbnav.sqlite')))

        self.assertEquals(
            True,
            con.connected()
        )

        con.close()
