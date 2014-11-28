#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest

from tests.testcase import DbTestCase
from dbnav import exception


def load_suite():
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromTestCase(ExceptionTestCase)
    return suite


class ExceptionTestCase(DbTestCase):
    def test_prefixes(self):
        """Tests the exception.unknown_column_message function"""

        con = DbTestCase.connection
        user = con.table('user')
        blog = con.table('blog')

        self.assertEqual(
            'Column "name" was not found on table "user" '
            '(close matches: username, last_name)',
            exception.unknown_column_message(user, 'name'))
        self.assertEqual(
            'Column "me" was not found on table "blog" '
            '(close matches: name)',
            exception.unknown_column_message(blog, 'me'))
        self.assertEqual(
            'Column "foo" was not found on table "blog" '
            '(no close matches in: id, name, url)',
            exception.unknown_column_message(blog, 'foo'))
