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

from datetime import datetime

from tests.testcase import DbTestCase
from tests.mock.sources import MockSource
from dbmanagr import options


class OptionsTestCase(DbTestCase):
    def test_escape_keyword(self):
        """Tests the options.escape_keyword function"""

        self.assertEqual(
            'a',
            options.escape_keyword('a'))
        self.assertEqual(
            '"user"',
            options.escape_keyword('user'))
        self.assertEqual(
            '"table"',
            options.escape_keyword('table'))

    def test_format_value(self):
        """Tests the options.format_value function"""

        DbTestCase.connection.close()
        DbTestCase.connection = MockSource().list()[0]
        DbTestCase.connection.connect()
        con = DbTestCase.connection
        user = con.table('user')
        user2 = con.table('user2')
        article = con.table('article')
        now = datetime.now()

        self.assertEqual(
            u'null',
            options.format_value(None, None)
        )
        self.assertEqual(
            '1',
            options.format_value(None, 1)
        )
        self.assertEqual(
            "'d'",
            options.format_value(None, 'd')
        )
        self.assertEqual(
            u'7',
            options.format_value(user.column('id'), 7)
        )
        self.assertEqual(
            u"'a'",
            options.format_value(user.column('id'), 'a')
        )
        self.assertEqual(
            'null',
            options.format_value(user.column('id'), None)
        )
        self.assertEqual(
            'true',
            options.format_value(user2.column('deleted'), True)
        )
        self.assertEqual(
            '3.141500',
            options.format_value(user2.column('score'), 3.1415)
        )
        self.assertEqual(
            "'3.14.15'",
            options.format_value(user2.column('score'), '3.14.15')
        )
        self.assertEqual(
            "'{}'".format(str(now)),
            options.format_value(article.column('created'), now)
        )
        self.assertEqual(
            "('a', 'b')",
            options.format_value(article.column('id'), ['a', 'b'])
        )
        self.assertEqual(
            u"'[BLOB]'",
            options.format_value(article.column('id'), buffer('abc'))
        )

    def test_restriction(self):
        """Tests the options.restriction function"""

        con = DbTestCase.connection
        user = con.table('user')

        self.assertEqual(
            u'a.id is null',
            options.restriction('a', user.column('id'), '=', None))
        self.assertEqual(
            u'id is null',
            options.restriction(None, user.column('id'), '=', None))
        self.assertEqual(
            u'a.id = 7',
            options.restriction('a', user.column('id'), '=', 7))
        self.assertEqual(
            u"a.id = 'a'",
            options.restriction('a', user.column('id'), '=', 'a'))
        self.assertEqual(
            u"id = 'a'",
            options.restriction(None, user.column('id'), '=', 'a'))
        self.assertRaises(
            Exception,
            options.restriction,
            None, None, None, None
        )

    def test_options_parser(self):
        """Tests the options OptionsParser class"""

        self.assertEqual(
            None,
            options.OptionsParser().parse(None)
        )
