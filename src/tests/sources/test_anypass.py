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

from tests.testcase import ParentTestCase
from dbnav.sources import anypass
from dbnav.driver.sqlite.databaseconnection import SQLiteConnection

DIR = path.dirname(__file__)
RESOURCES = path.join(DIR, '../resources')
MYPASS_CONFIG = path.join(RESOURCES, 'mypass')
MYPASS_CONFIG_404 = path.join(RESOURCES, 'mypass-404')
SQLITEPASS_CONFIG = path.join(RESOURCES, 'sqlitepass')
SQLITEPASS_CONFIG_404 = path.join(RESOURCES, 'sqlitepass-404')


class OptionsTestCase(ParentTestCase):
    def test_anypass_list(self):
        """Tests the anypass.AnyPassSource.list method"""

        self.assertEqual(
            ['dbnav.sqlite/'],
            map(str, anypass.AnyPassSource(
                '', MYPASS_CONFIG, SQLiteConnection).list()))
        self.assertEqual(
            [],
            map(str, anypass.AnyPassSource(
                '', MYPASS_CONFIG_404, None).list()))

    def test_anyfilepass_list(self):
        """Tests the anypass.AnyFilePassSource.list method"""

        self.assertEqual(
            ['dbnav.sqlite/'],
            map(str, anypass.AnyFilePassSource(
                '', SQLITEPASS_CONFIG, SQLiteConnection).list()))
        self.assertEqual(
            [],
            map(str, anypass.AnyFilePassSource(
                '', SQLITEPASS_CONFIG_404, SQLiteConnection).list()))
