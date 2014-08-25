#!/usr/bin/env python
# -*- coding: utf-8 -*-

import glob
import unittest

from os import path
from dbnav.tests.generator import test_generator, params
from dbnav import navigator
from dbnav.postgresql import init_postgresql
from dbnav.sqlite import init_sqlite
from dbnav.writer import StringWriter, Writer
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

def escape(s):
    if type(s) == unicode:
        return s.replace('"', '&quot;')
    return s

class TestWriter(StringWriter):
    ITEMS_FORMAT = u"""Title\tAutocomplete
{0}"""
    ITEM_FORMAT = u"""{title}\t{autocomplete}
"""
    def str(self, items):
        s = u''.join([self.itemtostring(i) for i in items])
        return TestWriter.ITEMS_FORMAT.format(s)
    def itemtostring(self, item):
        return TestWriter.ITEM_FORMAT.format(**item.escaped(escape))
    def write(self, items):
        return self.str(items)

Writer.set(TestWriter())

class OutputTestCase(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None

def load_suite():
    for tc in TEST_CASES:
        test_name = 'test_%s' % tc.replace('-', '_')
        test = test_generator(navigator, 'dbnav', DIR, tc)
        test.__doc__ = 'Params: "%s"' % params(DIR, tc)
        setattr(OutputTestCase, test_name, test)
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromTestCase(OutputTestCase)
    return suite
