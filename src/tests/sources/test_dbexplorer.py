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
from dbmanagr.sources import dbexplorer
from dbmanagr.driver.mysql.databaseconnection import MySQLConnection

DIR = path.dirname(__file__)
RESOURCES = path.join(DIR, '../resources')
DBEXPLORER_CONFIG = path.join(RESOURCES, 'dbexplorer.cfg')
DBEXPLORER_CONFIG_BROKEN = path.join(RESOURCES, 'dbexplorer-broken.cfg')
DBEXPLORER_CONFIG_404 = path.join(RESOURCES, 'dbexplorer-404.cfg')
MYPASS_CONFIG = path.join(RESOURCES, 'mypass')
MYPASS_CONFIG_404 = path.join(RESOURCES, 'mypass-404')


class SourcesTestCase(ParentTestCase):
    def test_dbexplorer_list(self):
        """Tests the dbexplorer.DBExplorerSource.list method"""

        self.assertEqual(
            [],
            map(str, dbexplorer.DBExplorerSource(
                '',
                DBEXPLORER_CONFIG,
                'mysql',
                MySQLConnection).list()))
        self.assertEqual(
            [],
            map(str, dbexplorer.DBExplorerSource(
                '',
                DBEXPLORER_CONFIG_BROKEN,
                'mysql',
                MySQLConnection).list()))
        self.assertEqual(
            [],
            map(str, dbexplorer.DBExplorerSource(
                '',
                DBEXPLORER_CONFIG_404,
                'mysql',
                MySQLConnection).list()))
