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

import unittest

from os import path

from tests.testcase import ParentTestCase
from dbnav.postgresql import sources

DIR = path.dirname(__file__)
RESOURCES = path.join(DIR, '../resources')
DBEXPLORER_CONFIG = path.join(RESOURCES, 'dbexplorer.cfg')
DBEXPLORER_CONFIG_BROKEN = path.join(RESOURCES, 'dbexplorer-broken.cfg')
DBEXPLORER_CONFIG_404 = path.join(RESOURCES, 'dbexplorer-404.cfg')
NAVICAT_CONFIG = path.join(RESOURCES, 'navicat.plist')
NAVICAT_CONFIG_404 = path.join(RESOURCES, 'navicat-404.plist')


def load_suite():
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromTestCase(SourcesTestCase)
    return suite


class SourcesTestCase(ParentTestCase):
    def test_dbexplorer_list(self):
        """Tests the postgresql.DBExplorerPostgreSQLSource.list class"""

        self.assertEqual(
            [],
            map(str, sources.DBExplorerPostgreSQLSource(
                '', DBEXPLORER_CONFIG).list()))
        self.assertEqual(
            [],
            map(str, sources.DBExplorerPostgreSQLSource(
                '', DBEXPLORER_CONFIG_BROKEN).list()))
        self.assertEqual(
            [],
            map(str, sources.DBExplorerPostgreSQLSource(
                '', DBEXPLORER_CONFIG_404).list()))

    def test_navicat_list(self):
        """Tests the postgresql.NavicatSQLiteSource.list class"""

        self.assertEqual(
            [],
            map(str, sources.NavicatPostgreSQLSource(
                '', NAVICAT_CONFIG).list()))
        self.assertEqual(
            [],
            map(str, sources.NavicatPostgreSQLSource(
                '', NAVICAT_CONFIG_404).list()))
