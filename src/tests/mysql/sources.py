#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest

from os import path

from tests.testcase import ParentTestCase
from dbnav.mysql import sources

DIR = path.dirname(__file__)
RESOURCES = path.join(DIR, '../resources')
DBEXPLORER_CONFIG = path.join(RESOURCES, 'dbexplorer.cfg')
DBEXPLORER_CONFIG_BROKEN = path.join(RESOURCES, 'dbexplorer-broken.cfg')
DBEXPLORER_CONFIG_404 = path.join(RESOURCES, 'dbexplorer-404.cfg')
MYPASS_CONFIG = path.join(RESOURCES, 'mypass')
MYPASS_CONFIG_404 = path.join(RESOURCES, 'mypass-404')


def load_suite():
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromTestCase(SourcesTestCase)
    return suite


class SourcesTestCase(ParentTestCase):
    def test_dbexplorer_list(self):
        """Tests the mysql.DBExplorerMySQLSource.list class"""

        self.assertEqual(
            [],
            map(str, sources.DBExplorerMySQLSource(
                '', DBEXPLORER_CONFIG).list()))
        self.assertEqual(
            [],
            map(str, sources.DBExplorerMySQLSource(
                '', DBEXPLORER_CONFIG_BROKEN).list()))
        self.assertEqual(
            [],
            map(str, sources.DBExplorerMySQLSource(
                '', DBEXPLORER_CONFIG_404).list()))

    def test_mypass_list(self):
        """Tests the mysql.MypassSource.list class"""

        self.assertEqual(
            [],
            map(str, sources.MypassSource(
                '', MYPASS_CONFIG).list()))
        self.assertEqual(
            [],
            map(str, sources.MypassSource(
                '', MYPASS_CONFIG_404).list()))
