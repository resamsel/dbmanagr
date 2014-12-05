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

import os

from tests.testcase import DbTestCase
from tests.navigator import load
from dbnav import navigator
from dbnav.config import Config
from dbnav.exception import UnknownTableException


def test_navigator():
    os.environ['UNITTEST'] = 'True'
    for test in load():
        yield test,
    del os.environ['UNITTEST']


class NavigatorTestCase(DbTestCase):
    def test_trace(self):
        """Tests the trace option"""

        self.assertEqual(
            True,
            Config.init(['-l', 'trace'], navigator.args.parser).trace)

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
