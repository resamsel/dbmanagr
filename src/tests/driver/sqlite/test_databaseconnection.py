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
from dbnav.driver import sqlite
from dbnav.driver.sqlite import databaseconnection as dbc
from dbnav.driver import DatabaseDriver


class Opts(DatabaseDriver):
    def __init__(
            self, uri=None, user=None, password=None, host=None, gen=None):
        self.uri = uri
        self.user = user
        self.password = password
        self.host = host
        self.gen = gen


class DatabaseConnectionTestCase(DbTestCase):
    def test_init(self):
        """Tests the init function"""

        driver, sqlite.DRIVERS = sqlite.DRIVERS, {}
        self.assertIsNone(
            sqlite.init()
        )
        sqlite.DRIVERS = driver

    def test_matches(self):
        """Tests the matches method"""

        self.assertEqual(
            False,
            dbc.SQLiteConnection(
                'sqlite:////kkdkjfkdjk',
                None,
                None,
                '',
                None,
                None).matches(Opts()))
