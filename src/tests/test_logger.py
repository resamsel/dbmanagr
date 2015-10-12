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
import logging

from tests.testcase import ParentTestCase
import dbmanagr
from dbmanagr.logger import LogWith

logger = logging.getLogger(__name__)


def load_suite():
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromTestCase(LoggerTestCase)
    return suite


def test_no_debug():
    logger2 = logging.getLogger('nodebug')
    logger2.setLevel(logging.WARNING)

    @LogWith(logger2)
    def foo():
        return 'bar'
    assert foo() == 'bar'


class LoggerTestCase(ParentTestCase):
    def test_prefixes(self):
        """Tests the logger.encode function"""

        self.assertEqual(
            None,
            dbmanagr.logger.encode(None))
        self.assertEqual(
            "u'a'",
            dbmanagr.logger.encode(u'a'))
        self.assertEqual(
            "'a'",
            dbmanagr.logger.encode('a'))
        self.assertEqual(
            ["'a.b'"],
            dbmanagr.logger.encode(['a.b']))
        self.assertEqual(
            "7",
            dbmanagr.logger.encode(7))

    def test_argtostring(self):
        """Tests the logger.argtostring function"""

        self.assertEqual(
            "k='v'",
            dbmanagr.logger.argtostring('k', 'v'))
        self.assertEqual(
            "self",
            dbmanagr.logger.argtostring('self', 'v'))
        self.assertEqual(
            "k=[\"'v1'\", \"'v2'\"]",
            dbmanagr.logger.argtostring('k', ['v1', 'v2']))
        self.assertEqual(
            "k=None",
            dbmanagr.logger.argtostring('k', None))
