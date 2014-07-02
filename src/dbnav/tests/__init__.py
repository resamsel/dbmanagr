#!/usr/bin/env python
# -*- coding: utf-8 -*-

from os import path
import unittest
from dbnav import navigator
from dbnav.sources import Source
from dbnav.writer import *
from dbnav.postgresql import init_postgresql
from dbnav.sqlite import init_sqlite
import glob
import codecs

DIR = path.dirname(__file__)
TEST_CASES = map(lambda p: path.basename(p), glob.glob(path.join(DIR, 'resources/testcase-*')))

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

def params(testcase):
    with codecs.open(path.join(DIR, 'resources/%s' % testcase), encoding='utf-8', mode='r') as f:
        return f.read()

def expected(testcase):
    with codecs.open(path.join(DIR, 'resources/expected/%s' % testcase), encoding='utf-8', mode='r') as f:
        return f.read()

def update_expected(testcase, content):
    with codecs.open(path.join(DIR, 'resources/expected/%s' % testcase), encoding='utf-8', mode='w') as f:
        return f.write(content)

class OutputTestCase(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None

def test_generator(tc):
    def test(self):
        p, e = params(tc), expected(tc)
        items = navigator.run(['dbnav',
            '-l', 'debug',
            '-f', 'target/dbnavigator.log',
            p])
        actual = Writer.write(items)

        # WARNING: this is code that creates the expected output - only uncomment when in need!
        #update_expected(tc, actual)

        self.assertEqual(e, actual)
    return test

def load_suite():
    for tc in TEST_CASES:
        test_name = 'test_%s' % tc.replace('-', '_')
        test = test_generator(tc)
        test.__doc__ = 'Params: "%s"' % params(tc)
        setattr(OutputTestCase, test_name, test)
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromTestCase(OutputTestCase)
    return suite
