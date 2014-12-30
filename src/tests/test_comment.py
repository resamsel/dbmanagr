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
        """Tests the comment.update_aliases function"""

        con = DbTestCase.connection
        user = con.table('user')
        blog_user = con.table('blog_user')
        aliases = OrderedDict()
        c = Counter()

        self.assertEqual(
            {},
            comment.update_aliases(None, None, {}, {})
        )
        self.assertEqual(
            OrderedDict([('user', '_user')]),
            comment.update_aliases(
                'user_address', c, aliases, user.foreign_keys())
        )
        self.assertEqual(
            OrderedDict([('user', '_user'), ('blog', '_blog')]),
            comment.update_aliases(
                'blog_user', c, aliases, blog_user.foreign_keys())
        )
        self.assertEqual(
            {},
            comment.update_aliases(
                't3', c, {}, user.foreign_keys())
        )

    def test_create_alias(self):
        """Tests the comment.create_alias function"""

        c = Counter()
        comment.create_alias('a', c)

        self.assertEqual(
            '_a2',
            comment.create_alias('a', c)
        )

    def test_column_aliases(self):
        """Tests the comment.column_aliases function"""

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
        """Tests the comment.create_comment function"""

        con = DbTestCase.connection
        user = con.table('user')
        user_comment = con.comment('user')
        c = Counter()

        self.assertEqual(
            '{_user_id}',  # comment.Comment('id', ),
            comment.create_comment(
                user,
                user_comment,
                c,
                {},
                '_user').id
        )

        pk, user.primary_key = user.primary_key, False
        self.assertEqual(
            '-',  # comment.Comment('id', ),
            comment.create_comment(
                user,
                user_comment,
                c,
                {},
                '_user').id
        )
        user.primary_key = pk

        user_comment.id = '{id}'
        self.assertEqual(
            '{_user_id}',  # comment.Comment('id', ),
            comment.create_comment(
                user,
                user_comment,
                c,
                {},
                '_user').id
        )
