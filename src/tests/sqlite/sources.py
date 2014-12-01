#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest

from os import path

from tests.testcase import ParentTestCase
from dbnav.sqlite import sources

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
        """Tests the sqlite.DBExplorerSQLiteSource.list class"""

        self.assertEqual(
            ['Rene.Samselnig@gmail.com.sqlite/'],
            map(str, sources.DBExplorerSQLiteSource(
                '', DBEXPLORER_CONFIG).list()))
        self.assertEqual(
            [],
            map(str, sources.DBExplorerSQLiteSource(
                '', DBEXPLORER_CONFIG_BROKEN).list()))
        self.assertEqual(
            [],
            map(str, sources.DBExplorerSQLiteSource(
                '', DBEXPLORER_CONFIG_404).list()))

    def test_navicat_list(self):
        """Tests the sqlite.NavicatSQLiteSource.list class"""

        self.assertEqual(
            ['me@xyz.com.sqlite/', 'dbnav.sqlite/', 'dbnav-c.sqlite/'],
            map(str, sources.NavicatSQLiteSource(
                '', NAVICAT_CONFIG).list()))
        self.assertEqual(
            [],
            map(str, sources.NavicatSQLiteSource(
                '', NAVICAT_CONFIG_404).list()))
