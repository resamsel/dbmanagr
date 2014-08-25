#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest

import dbnav.tests.navigator
import dbnav.tests.grapher

def load_suite():
    suite = unittest.TestSuite()

    suite.addTest(navigator.load_suite())
    suite.addTest(grapher.load_suite())

    return suite
