#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest

from sqlalchemy import String

from tests.testcase import ParentTestCase
from tests.mock.sources import MockSource

from dbnav import querybuilder
from dbnav.model.column import Column


def load_suite():
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromTestCase(QueryBuilderTestCase)
    return suite


class QueryBuilderTestCase(ParentTestCase):
    connection = None

    @classmethod
    def set_up_class(cls):
        QueryBuilderTestCase.connection = MockSource().list()[1]
        QueryBuilderTestCase.connection.connect()

    @classmethod
    def tear_down_class(cls):
        QueryBuilderTestCase.connection.close()
        QueryBuilderTestCase.connection = None

    def test_allowed(self):
        """Tests the utils.allowed function"""

        self.assertEqual(
            True,
            querybuilder.allowed(Column(None, 'c1', type=String()), '~', None))
        self.assertEqual(
            False,
            querybuilder.allowed(Column(None, 'c1', type=int), '~', None))
        self.assertEqual(
            True,
            querybuilder.allowed(Column(None, 'c1', type=int), '=', 1))
        self.assertEqual(
            True,
            querybuilder.allowed(Column(None, 'c1', type=int), ':', [1, 2, 3]))

    def test_add_references(self):
        """Tests the utils.add_references function"""

        con = QueryBuilderTestCase.connection
        user = con.table('user')
        user_address = con.table('user_address')

        self.assertEqual(
            ['user'],
            querybuilder.add_references(
                user_address.name, user.foreign_keys(), {}, None).keys())

    def test_add_joins(self):
        """Tests the utils.add_joins function"""

        con = QueryBuilderTestCase.connection

        self.assertEqual(
            ['user'],
            querybuilder.add_join(con.entity('user'), {}).keys())
        self.assertEqual(
            ['user_address'],
            querybuilder.add_join(con.entity('user_address'), {}).keys())
