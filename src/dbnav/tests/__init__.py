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

Writer.set(StringWriter())
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
        self.assertEqual(e, Writer.write(items))
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
