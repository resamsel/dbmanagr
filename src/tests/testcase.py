#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
import os


class ParentTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):  # noqa
        os.environ['UNITTEST'] = 'True'

    @classmethod
    def tearDownClass(cls):  # noqa
        del os.environ['UNITTEST']

    def setUp(self):  # noqa
        self.maxDiff = None
