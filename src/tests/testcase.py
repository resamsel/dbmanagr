#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright © 2014 René Samselnig
#
# This file is part of Database Navigator.
#
# Database Navigator is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Database Navigator is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Database Navigator.  If not, see <http://www.gnu.org/licenses/>.
#

import unittest
import os

from tests.mock.sources import MockSource


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


class DbTestCase(ParentTestCase):
    connection = None

    @classmethod
    def set_up_class(cls):
        DbTestCase.connection = MockSource().list()[1]
        DbTestCase.connection.connect()

    @classmethod
    def tear_down_class(cls):
        DbTestCase.connection.close()
        DbTestCase.connection = None
