#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
import os


class ParentTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):  # noqa
        os.environ['UNITTEST'] = 'True'
        cls.set_up_class()

    @classmethod
    def tearDownClass(cls):  # noqa
        cls.tear_down_class()
        del os.environ['UNITTEST']

    @classmethod
    def set_up_class(cls):
        pass

    @classmethod
    def tear_down_class(cls):
        pass

    def setUp(self):  # noqa
        self.maxDiff = None
