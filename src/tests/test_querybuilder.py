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

from collections import OrderedDict

from tests.testcase import DbTestCase

from dbnav import querybuilder
from dbnav import queryfilter
from dbnav.exception import UnknownColumnException

logger = logging.getLogger(__name__)


def load_suite():
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromTestCase(QueryBuilderTestCase)
    return suite


class QueryBuilderTestCase(DbTestCase):
    def test_allowed(self):
        """Tests the querybuilder.allowed function"""

        con = DbTestCase.connection
        user = con.entity('user')

        self.assertEqual(
            True,
            querybuilder.allowed(user.columns.username, '~', None))
        self.assertEqual(
            False,
            querybuilder.allowed(user.columns.id, '~', None))
        self.assertEqual(
            True,
            querybuilder.allowed(user.columns.id, '=', 1))
        self.assertEqual(
            True,
            querybuilder.allowed(user.columns.id, ':', [1, 2, 3]))
        self.assertEqual(
            False,
            querybuilder.allowed(user.columns.id, '=', 'd'))

    def test_add_references(self):
        """Tests the querybuilder.add_references function"""

        con = DbTestCase.connection
        user = con.table('user')
        user_address = con.table('user_address')

        self.assertEqual(
            ['user'],
            querybuilder.add_references(
                user_address.name, user.foreign_keys(), {}, None).keys())

    def test_add_joins(self):
        """Tests the querybuilder.add_joins function"""

        con = DbTestCase.connection
        joins = OrderedDict()

        self.assertEqual(
            ['user'],
            querybuilder.add_join(con.entity('user'), {}).keys())
        self.assertEqual(
            ['user_address'],
            querybuilder.add_join(con.entity('user_address'), joins).keys())
        self.assertEqual(
            ['user_address', 'user'],
            querybuilder.add_join(con.entity('user'), joins).keys())
        self.assertEqual(
            ['user_address', 'user', 'address'],
            querybuilder.add_join(con.entity('address'), joins).keys())
        # Add the same entity a second time
        self.assertEqual(
            ['user_address', 'user', 'address'],
            querybuilder.add_join(con.entity('address'), joins).keys())

    def test_add_filter(self):
        """Tests the querybuilder.add_filter function"""

        con = DbTestCase.connection
        user = con.table('user')

        self.assertEqual(
            None,
            querybuilder.add_filter(
                queryfilter.QueryFilter(None, None, None), None, None, None))
        self.assertRaises(
            UnknownColumnException,
            querybuilder.add_filter,
            queryfilter.QueryFilter('unknown', '=', 7), [], user, {})
        self.assertRaises(
            UnknownColumnException,
            querybuilder.add_filter,
            queryfilter.QueryFilter('unknown.id', '=', 7), [], user, {})

    def test_replace_filter(self):
        """Tests the querybuilder.replace_filter function"""

        # Line 111 of querybuilder needs to be tested
        pass

    def test_create_label(self):
        """Tests the querybuilder.create_label function"""

        con = DbTestCase.connection
        column = con.entity('user').columns.id

        self.assertEqual(
            'id',
            querybuilder.create_label('{col.name}')(column).name)
        self.assertEqual(
            '_id',
            querybuilder.create_label('_{col.name}')(column).name)
        self.assertEqual(
            '_user_id',
            querybuilder.create_label(
                '_{col.table.name}_{col.name}')(column).name)

    def test_operation(self):
        """Tests the querybuilder.operation function"""

        con = DbTestCase.connection
        column = con.entity('user').columns.id
        v = 1

        self.assertEqual(
            str(column == v),
            str(querybuilder.operation(column, '=', v)))

    def test_column_or_raise(self):
        """Tests the querybuilder.column_or_raise function"""

        con = DbTestCase.connection
        table = con.table('user')

        self.assertRaises(
            UnknownColumnException,
            querybuilder.column_or_raise,
            table,
            'unknown'
        )

    def test_simplify(self):
        """Tests the querybuilder.simplify function"""

        con = DbTestCase.connection
        table = con.table('user')

        self.assertIsNone(
            querybuilder.simplify(table, None, 'a', {'first_name': 'John'})
        )

    def test_build(self):
        """Tests the querybuilder.QueryBuilder.build method"""

        con = DbTestCase.connection
        blog_user = con.table('blog_user')
        self.assertIsNotNone(
            querybuilder.QueryBuilder(con, blog_user, limit=1).build()
        )
