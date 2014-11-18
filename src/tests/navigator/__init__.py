#!/usr/bin/env python
# -*- coding: utf-8 -*-

import glob
import unittest
import os

from os import path
from tests.generator import test_generator, params
from tests.sources import init_sources
from dbnav import navigator

DIR = path.dirname(__file__)
TEST_CASES = map(
    lambda p: path.basename(p),
    glob.glob(path.join(DIR, 'resources/testcase-*')))

init_sources(DIR)


class OutputTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):  # noqa
        os.environ['UNITTEST'] = 'True'

    @classmethod
    def tearDownClass(cls):  # noqa
        del os.environ['UNITTEST']

    def setUp(self):  # noqa
        self.maxDiff = None


def load_suite():
    command = 'dbnav'
    for tc in TEST_CASES:
        test_name = 'test_%s_%s' % (command, tc.replace('-', '_'))
        test = test_generator(navigator, command, DIR, tc, ['-T'])
        test.__doc__ = 'Params: "%s"' % params(DIR, tc)
        setattr(OutputTestCase, test_name, test)
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromTestCase(OutputTestCase)
    return suite
