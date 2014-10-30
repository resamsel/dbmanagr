#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest

import tests.navigator
import tests.grapher
import tests.exporter
import tests.differ

def load_suite():
    suite = unittest.TestSuite()

    suite.addTest(navigator.load_suite())
    suite.addTest(grapher.load_suite())
    suite.addTest(exporter.load_suite())
    suite.addTest(differ.load_suite())

    return suite
