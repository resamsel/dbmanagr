#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest

from tests.testcase import ParentTestCase
from dbnav import utils


class UtilsTestCase(ParentTestCase):
    def test_prefixes(self):
        self.assertEqual(
            set(['a']),
            utils.prefixes(['a.b']))
        self.assertEqual(
            set(['a', 'b']),
            utils.prefixes(['a.b', 'a.c', 'b']))
        self.assertEqual(
            set(['a', 'b', 'c']),
            utils.prefixes(['a.b', 'b.c', 'b', 'c.c']))

    def test_remove_prefix(self):
        self.assertEqual(
            ['b'],
            utils.remove_prefix('a', ['a.b', 'b.c', 'b', 'b.b', 'c.c', 'c.d']))
        self.assertEqual(
            ['c', 'b'],
            utils.remove_prefix('b', ['a.b', 'b.c', 'b', 'b.b', 'c.c', 'c.d']))
        self.assertEqual(
            ['c', 'd'],
            utils.remove_prefix('c', ['a.b', 'b.c', 'b', 'b.b', 'c.c', 'c.d']))


def load_suite():
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromTestCase(UtilsTestCase)
    return suite
