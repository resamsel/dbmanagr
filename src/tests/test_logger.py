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
import dbnav
from dbnav.logger import LogWith

logger = logging.getLogger(__name__)


def load_suite():
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromTestCase(LoggerTestCase)
    return suite


def test_no_debug():
    @LogWith(logger)
    def foo():
        return 'bar'
    assert foo() == 'bar'


class LoggerTestCase(ParentTestCase):
    def test_prefixes(self):
        """Tests the logger.encode function"""

        self.assertEqual(
            None,
            dbnav.logger.encode(None))
        self.assertEqual(
            "u'a'",
            dbnav.logger.encode(u'a'))
        self.assertEqual(
            "u'a'",
            dbnav.logger.encode('a'))
        self.assertEqual(
            ["u'a.b'"],
            dbnav.logger.encode(['a.b']))
        self.assertEqual(
            "u'7'",
            dbnav.logger.encode(7))

    def test_argtostring(self):
        """Tests the logger.argtostring function"""

        self.assertEqual(
            "k=u'v'",
            dbnav.logger.argtostring('k', 'v'))
        self.assertEqual(
            "self",
            dbnav.logger.argtostring('self', 'v'))
        self.assertEqual(
            "k=[\"u'v1'\", \"u'v2'\"]",
            dbnav.logger.argtostring('k', ['v1', 'v2']))
        self.assertEqual(
            "k=None",
            dbnav.logger.argtostring('k', None))
