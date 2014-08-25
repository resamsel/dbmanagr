#!/usr/bin/env python
# -*- coding: utf-8 -*-

import glob
import unittest

from os import path
from dbnav.tests.generator import test_generator, params
from dbnav import grapher
from dbnav.postgresql import init_postgresql
from dbnav.sqlite import init_sqlite
from dbnav.writer import DefaultWriter
from dbnav.sources import Source

DIR = path.dirname(__file__)
TEST_CASES = map(lambda p: path.basename(p), glob.glob(path.join(DIR, 'resources/testcase-*')))

Source.sources = []
init_postgresql(
    path.join(DIR, 'resources/dbexplorer.cfg'),
    path.join(DIR, 'resources/pgpass'),
    path.join(DIR, 'resources/navicat.plist')
)
init_sqlite(
    path.join(DIR, 'resources/dbexplorer.cfg'),
    path.join(DIR, 'resources/navicat.plist')
)

DefaultWriter.PRINT = False

class OutputTestCase(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None

def load_suite():
    for tc in TEST_CASES:
        test_name = 'test_%s' % tc.replace('-', '_')
        test = test_generator(grapher, 'dbgraph', DIR, tc)
        test.__doc__ = 'Params: "%s"' % params(DIR, tc)
        setattr(OutputTestCase, test_name, test)
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromTestCase(OutputTestCase)
    return suite
