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

from dbmanagr.command import navigator
from tests.testcase import DbTestCase
from tests.command.navigator import load
from dbmanagr.config import Config
from dbmanagr.exception import UnknownTableException
from dbmanagr.utils import mute_stderr, hash_


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
            Config.init(['--trace'], navigator.args.parser).trace)

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
        options = Config.init(
            ['dbmanagr-c.sqlite/user'], navigator.args.parser)

        options.show = 'connections'
        self.assertEqual(
            [None],
            navigator.create(None, options))

        options.show = 'databases'
        self.assertEqual(
            ['dbmanagr-c.sqlite//'],
            map(str, navigator.create(con, options)))

        options.database = 'db'
        self.assertEqual(
            [],
            map(str, navigator.create(con, options)))

        options = Config.init(
            ['dbmanagr-c.sqlite/user?'], navigator.args.parser)
        self.assertEqual(
            ['dbmanagr-c.sqlite/'],
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
        options = Config.init(
            ['dbmanagr-c.sqlite/user?'], navigator.args.parser)
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
            navigator.main(['dbmanagr.sqlite/unknown?']))

    def test_execute(self):
        """Tests the navigator.execute function"""

        self.assertRaises(
            SystemExit,
            mute_stderr(navigator.execute),
            ['-K']
        )

    def test_to_dto(self):
        """Tests the navigator.dto.to_dto function"""

        self.assertEqual({}, navigator.dto.to_dto({}))
        self.assertEqual('a', navigator.dto.to_dto('a'))

    def test_item(self):
        """Tests the navigator.dto.Item class"""

        item = navigator.dto.Item(
            title='a',
            subtitle='b',
            autocomplete='c',
            uid='d',
            icon='e',
            value='f',
            validity='g',
            format_='h'
        )

        self.assertEqual(item, item)
        self.assertEqual(hash(item), item.__hash__())
        self.assertEqual('a', item.title())
        self.assertEqual('b', item.subtitle())
        self.assertEqual('c', item.autocomplete())
        self.assertEqual('d', item.uid())
        self.assertEqual('e', item.icon())
        self.assertEqual('f', item.value())
        self.assertEqual('g', item.validity())
        self.assertEqual('h', item.format())
        self.assertEqual(
            hash_('c'),
            navigator.dto.Item(autocomplete='c').uid()
        )
        self.assertEqual(
            'images/icon.png',
            navigator.dto.Item().icon()
        )
        self.assertEqual(
            item,
            navigator.dto.Item.from_json({
                'title': 'a',
                'subtitle': 'b',
                'autocomplete': 'c',
                'uid': 'd',
                'icon': 'e',
                'value': 'f',
                'validity': 'g',
                'format_': 'h'
            })
        )
