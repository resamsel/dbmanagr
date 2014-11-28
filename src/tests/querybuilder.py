#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest

from collections import OrderedDict

from tests.testcase import DbTestCase

from dbnav import querybuilder


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
