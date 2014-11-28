#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest

from collections import OrderedDict

from tests.testcase import DbTestCase
from dbnav.model import databaseconnection as dbc
from dbnav.model.row import Row


def load_suite():
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromTestCase(DatabaseConnectionTestCase)
    return suite


class ResultRow:
    def __init__(self, d):
        self.__dict__ = d

    def keys(self):
        return self.__dict__.keys() + range(len(self.__dict__.keys()))

    def __getitem__(self, i):
        if type(i) is int:
            return self.__dict__[self.__dict__.keys()[i]]
        return self.__dict__[i]


class DatabaseConnectionTestCase(DbTestCase):
    def test_foreign_key_or_column(self):
        """Tests the databaseconnection.foreign_key_or_column function"""

        con = DbTestCase.connection
        user = con.table('user')
        article = con.table('article')

        self.assertEqual(
            user.column('id'),
            dbc.foreign_key_or_column(user, 'id'))
        self.assertEqual(
            article.foreign_key('user_id'),
            dbc.foreign_key_or_column(article, 'user_id'))
        self.assertEqual(
            None,
            dbc.foreign_key_or_column(article, 'foo'))

    def test_val(self):
        """Tests the databaseconnection.foreign_key_or_column function"""

        con = DbTestCase.connection
        user = con.table('user')
        row = Row(user, ResultRow(OrderedDict([('id', 1), ('foo', 'Bar')])))

        self.assertEqual(
            None, dbc.val(row, 'bar'))
        self.assertEqual(
            1, dbc.val(row, 'id'))
        self.assertEqual(
            'Bar', dbc.val(row, 'foo'))
        self.assertEqual(
            'Bar', row['foo'])
        self.assertEqual(
            None, row['bar'])
        self.assertEqual(
            'Bar', dbc.val(row, 1))

    def test_forward_references(self):
        """Tests the databaseconnection.forward_references function"""

        con = DbTestCase.connection
        article = con.table('article')
        row = article.rows(con, limit=1)[0]
        aliases = {'article': '_article'}

        self.assertEqual(558, row['user_id'])
        self.assertEqual(
            [558],
            map(lambda v: v.value(),
                dbc.forward_references(
                    row, article, ['user_id'], aliases)))

    def test_back_references(self):
        """Tests the databaseconnection.forward_references function"""

        con = DbTestCase.connection
        user = con.table('user')
        row = user.rows(con, limit=1)[0]
        aliases = {'user': '_user'}

        self.assertEqual(
            ['article.user_id', 'blog_user.user_id', 'user_address.user_id'],
            map(lambda v: str(v.value()),
                dbc.back_references(row, user, aliases)))
