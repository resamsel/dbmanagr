#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest

from tests.testcase import ParentTestCase
from dbnav import options


def load_suite():
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromTestCase(OptionsTestCase)
    return suite


class OptionsTestCase(ParentTestCase):
    def test_escape_keyword(self):
        """Tests the options.escape_keyword function"""

        self.assertEqual(
            'a',
            options.escape_keyword('a'))
        self.assertEqual(
            '"user"',
            options.escape_keyword('user'))
        self.assertEqual(
            '"table"',
            options.escape_keyword('table'))
