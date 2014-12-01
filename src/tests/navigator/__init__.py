#!/usr/bin/env python
# -*- coding: utf-8 -*-

import glob
import unittest

from os import path
from tests.generator import test_generator, params
from tests.sources import init_sources
from tests.testcase import ParentTestCase
from dbnav import navigator
from dbnav.exception import UnknownTableException

DIR = path.dirname(__file__)
TEST_CASES = map(
    lambda p: path.basename(p),
    glob.glob(path.join(DIR, 'resources/testcase-*')))

init_sources(DIR)


class OutputTestCase(ParentTestCase):
    pass


def load_suite():
    command = 'dbnav'
    for tc in TEST_CASES:
        test_name = 'test_%s_%s' % (command, tc.replace('-', '_'))
        test = test_generator(navigator, command, DIR, tc, ['-T'])
        test.__doc__ = 'Params: "%s"' % params(DIR, tc)
        setattr(OutputTestCase, test_name, test)
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromTestCase(OutputTestCase)
    suite.addTest(
        unittest.TestLoader().loadTestsFromTestCase(NavigatorTestCase))
    return suite


class NavigatorTestCase(ParentTestCase):
    def test_non_existent_table(self):
        self.assertRaises(
            UnknownTableException,
            navigator.run, ['me@xyz.com.sqlite/blog?'])
