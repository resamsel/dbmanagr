#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest

from tests import navigator
from tests import grapher
from tests import exporter
from tests import differ


def load_suite():
    suite = unittest.TestSuite()

    suite.addTest(navigator.load_suite())
    suite.addTest(grapher.load_suite())
    suite.addTest(exporter.load_suite())
    suite.addTest(differ.load_suite())

    return suite
