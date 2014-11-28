#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest

from tests.testcase import ParentTestCase
import dbnav


def load_suite():
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromTestCase(LoggerTestCase)
    return suite


class LoggerTestCase(ParentTestCase):
    def test_prefixes(self):
        """Tests the logger.encode function"""

        self.assertEqual(
            None,
            dbnav.logger.encode(None))
        self.assertEqual(
            u'a',
            dbnav.logger.encode(u'a'))
        self.assertEqual(
            u'a',
            dbnav.logger.encode('a'))
        self.assertEqual(
            [u'a.b'],
            dbnav.logger.encode(['a.b']))
        self.assertEqual(
            u'7',
            dbnav.logger.encode(7))

    def test_argtostring(self):
        """Tests the logger.argtostring function"""

        self.assertEqual(
            "k=v",
            dbnav.logger.argtostring('k', 'v'))
        self.assertEqual(
            "self",
            dbnav.logger.argtostring('self', 'v'))
        self.assertEqual(
            "k=[u'v1', u'v2']",
            dbnav.logger.argtostring('k', ['v1', 'v2']))
        self.assertEqual(
            "k=None",
            dbnav.logger.argtostring('k', None))
