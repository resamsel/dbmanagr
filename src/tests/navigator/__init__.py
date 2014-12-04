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

import glob
import unittest

from os import path
from tests.generator import test_generator, params
from tests.sources import init_sources
from tests.testcase import DbTestCase, ParentTestCase
from dbnav import navigator
from dbnav.exception import UnknownTableException

DIR = path.dirname(__file__)
TEST_CASES = map(
    lambda p: path.basename(p),
    glob.glob(path.join(DIR, 'resources/testcase-*')))

init_sources(DIR)


class OutputTestCase(ParentTestCase):
    pass


def load_suite():
    command = 'dbnav'
    for tc in TEST_CASES:
        test_name = 'test_%s_%s' % (command, tc.replace('-', '_'))
        test = test_generator(navigator, command, DIR, tc, ['-T'])
        test.__doc__ = 'Params: "%s"' % params(DIR, tc)
        setattr(OutputTestCase, test_name, test)
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromTestCase(OutputTestCase)
    suite.addTest(
        unittest.TestLoader().loadTestsFromTestCase(NavigatorTestCase))
    return suite


class NavigatorTestCase(DbTestCase):
    def test_non_existent_table(self):
        self.assertRaises(
            UnknownTableException,
            navigator.run, ['me@xyz.com.sqlite/blog?'])

    def test_forward_references(self):
        """Tests the navigator.forward_references function"""

        con = DbTestCase.connection
        article = con.table('article')
        row = article.rows(con, limit=1)[0]
        aliases = {'article': '_article'}

        self.assertEqual(558, row['user_id'])
        self.assertEqual(
            [558],
            map(lambda v: v.value(),
                navigator.forward_references(
                    row, article, ['user_id'], aliases)))

    def test_back_references(self):
        """Tests the navigator.back_references function"""

        con = DbTestCase.connection
        user = con.table('user')
        row = user.rows(con, limit=1)[0]
        aliases = {'user': '_user'}

        self.assertEqual(
            ['article.user_id', 'blog_user.user_id', 'user_address.user_id'],
            map(lambda v: str(v.value()),
                navigator.back_references(row, user, aliases)))
