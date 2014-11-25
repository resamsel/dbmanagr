#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest

from collections import Counter, OrderedDict

from dbnav.model.column import Column
from dbnav import comment

from tests.testcase import DbTestCase


def load_suite():
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromTestCase(CommentTestCase)
    return suite


class CommentTestCase(DbTestCase):
    def test_update_aliases(self):
        """Tests the utils.update_aliases function"""

        con = DbTestCase.connection
        user = con.table('user')
        blog_user = con.table('blog_user')
        aliases = OrderedDict()
        c = Counter()

        self.assertEqual(
            {},
            comment.update_aliases(None, None, {}, {}))
        self.assertEqual(
            OrderedDict([('user', '_user')]),
            comment.update_aliases(
                'user_address', c, aliases, user.foreign_keys()))
        self.assertEqual(
            OrderedDict([('user', '_user'), ('blog', '_blog')]),
            comment.update_aliases(
                'blog_user', c, aliases, blog_user.foreign_keys()))
        self.assertEqual(
            {},
            comment.update_aliases(
                't3', c, {}, user.foreign_keys()))

    def test_column_aliases(self):
        """Tests the utils.column_aliases function"""

        self.assertEqual(
            {},
            comment.column_aliases([], 'alias'))
        self.assertEqual(
            {'asdf': '{alias_asdf}'},
            comment.column_aliases([Column(None, 'asdf', type=str)], 'alias'))
        self.assertEqual(
            {
                'asdf': '{_alias_asdf}',
                'qwer': '{_alias_qwer}',
                'uiop': '{_alias_uiop}'
            },
            comment.column_aliases(
                [
                    Column(None, 'asdf', type=str),
                    Column(None, 'qwer', type=str),
                    Column(None, 'uiop', type=str)
                ],
                '_alias'))

    def test_create_comment(self):
        """Tests the utils.create_comment function"""

        pass
