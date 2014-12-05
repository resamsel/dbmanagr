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

from tests.testcase import DbTestCase
from dbnav import options


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

        con = DbTestCase.connection
        user = con.table('user')

        self.assertEqual(
            u'null',
            options.format_value(None, None))
        self.assertEqual(
            u'7',
            options.format_value(user.column('id'), 7))
        self.assertEqual(
            u"'a'",
            options.format_value(user.column('id'), 'a'))
        self.assertEqual(
            'null',
            options.format_value(user.column('id'), None))

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
