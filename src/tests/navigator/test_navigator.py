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

from dbnav import navigator
from tests.testcase import DbTestCase
from tests.navigator import load
from dbnav.config import Config
from dbnav.exception import UnknownTableException
from dbnav.utils import mute_stderr


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
        """Tests non existent tables"""

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

    def test_create(self):
        """Tests the navigator.create function"""

        con = DbTestCase.connection
        options = Config.init(['dbnav-c.sqlite/user'], navigator.args.parser)

        options.show = 'connections'
        self.assertEqual(
            [None],
            navigator.create(None, options))

        options.show = 'databases'
        self.assertEqual(
            ['dbnav-c.sqlite//'],
            map(str, navigator.create(con, options)))

        options.database = 'db'
        self.assertEqual(
            [],
            map(str, navigator.create(con, options)))

        options = Config.init(['dbnav-c.sqlite/user?'], navigator.args.parser)
        self.assertEqual(
            ['dbnav-c.sqlite/'],
            map(str, navigator.create(con, options)))

    def test_filter_complete(self):
        """Tests the filter_complete"""

        self.assertRaises(
            Exception,
            navigator.filter_complete,
            None
        )

    def test_create_values(self):
        """Tests the create_values function"""

        con = DbTestCase.connection
        user = con.table('user')
        options = Config.init(['dbnav-c.sqlite/user?'], navigator.args.parser)
        options.simplify = False

        self.assertIsNotNone(
            navigator.create_values(con, user, options)
        )

    def test_writer(self):
        """Tests the writer"""

        import sys
        sys.argv = ['']

        self.assertRaises(
            SystemExit,
            mute_stderr(navigator.main),
            ['-K'])

        self.assertEqual(
            0,
            navigator.main())
        self.assertEqual(
            -1,
            navigator.main(['dbnav.sqlite/unknown?']))
