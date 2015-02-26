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

from tests.testcase import DbTestCase
from dbnav import utils
from dbnav.model.column import Column
from dbnav.comment import Comment


def load_suite():
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromTestCase(UtilsTestCase)
    return suite


class UtilsTestCase(DbTestCase):
    def test_module_installed(self):
        """Tests the utils.module_installed function"""

        self.assertEqual(
            None,
            utils.module_installed('foobar'))

    def test_prefixes(self):
        """Tests the utils.prefixes function"""

        self.assertEqual(
            set(['a']),
            utils.prefixes(['a.b']))
        self.assertEqual(
            set(['a', 'b']),
            utils.prefixes(['a.b', 'a.c', 'b']))
        self.assertEqual(
            set(['a', 'b', 'c']),
            utils.prefixes(['a.b', 'b.c', 'b', 'c.c']))

    def test_remove_prefix(self):
        """Tests the utils.remove_prefix function"""

        self.assertEqual(
            ['b'],
            utils.remove_prefix('a', ['a.b', 'b.c', 'b', 'b.b', 'c.c', 'c.d']))
        self.assertEqual(
            ['c', 'b'],
            utils.remove_prefix('b', ['a.b', 'b.c', 'b', 'b.b', 'c.c', 'c.d']))
        self.assertEqual(
            ['c', 'd'],
            utils.remove_prefix('c', ['a.b', 'b.c', 'b', 'b.b', 'c.c', 'c.d']))
        self.assertEqual(
            [],
            utils.remove_prefix('d', ['a.b', 'b.c', 'b', 'b.b', 'c.c', 'c.d']))
        self.assertEqual(
            [],
            utils.remove_prefix('', ['a.b', 'b.c', 'b', 'b.b', 'c.c', 'c.d']))

    def test_dictplus(self):
        """Tests the utils.dictplus function"""

        self.assertEqual(
            {'a': 'b', 'b': 'b', 'c': 'd'},
            utils.dictplus({'a': 'b', 'b': 'c', 'c': 'd'}, 'b', 'b'))
        self.assertEqual(
            {'a': 'b', 'b': 'c', 'c': 'd', 'd': 'e'},
            utils.dictplus({'a': 'b', 'b': 'c', 'c': 'd'}, 'd', 'e'))

    def test_dictsplus(self):
        """Tests the utils.dictsplus function"""

        self.assertEqual(
            [{'a': 'b', 'b': 'b', 'c': 'd'}],
            utils.dictsplus([{'a': 'b', 'b': 'c', 'c': 'd'}], 'b', 'b'))
        self.assertEqual(
            [{'a': 'b', 'b': 'c', 'c': 'd', 'd': 'e'}],
            utils.dictsplus([{'a': 'b', 'b': 'c', 'c': 'd'}], 'd', 'e'))

    def test_dictminus(self):
        """Tests the utils.dictminus function"""

        self.assertEqual(
            {'a': 'b', 'c': 'd'},
            utils.dictminus({'a': 'b', 'b': 'c', 'c': 'd'}, 'b', 'd'))
        self.assertEqual(
            {'a': 'b', 'b': 'c', 'c': 'd'},
            utils.dictminus({'a': 'b', 'b': 'c', 'c': 'd'}))

    def test_getorelse(self):
        """Tests the utils.getorelse function"""

        self.assertEqual(
            'a',
            utils.getorelse(None, 'a'))
        self.assertEqual(
            'b',
            utils.getorelse('b', 'a'))
        self.assertEqual(
            1,
            utils.getorelse(len('b'), 0))
        self.assertEqual(
            0,
            utils.getorelse(0, 1))
        self.assertEqual(
            False,
            utils.getorelse(False, True))

    def test_create_title(self):
        """Tests the utils.create_title function"""

        con = DbTestCase.connection
        table = con.table('user')

        self.assertEqual(
            None,
            utils.create_title(None, []))
        self.assertEqual(
            ('name', '{name}'),
            utils.create_title(None, [Column(table, 'name', type=str)]))
        self.assertEqual(
            ('my_name', '{my_name}'),
            utils.create_title(None, [Column(table, 'my_name', type=str)]))
        self.assertEqual(
            ('asdf', '{asdf}'),
            utils.create_title(None, [Column(table, 'asdf', type=str)]))
        self.assertEqual(
            ('id', '{_id}'),
            utils.create_title(
                Comment(
                    '_id', 'title', 'subtitle', 'order', 'search', 'display',
                    'columns', 'aliases'),
                []))
        self.assertEqual(
            ('id', '{_id}'),
            utils.create_title(
                Comment(
                    '_id', 'title', 'subtitle', 'order', 'search', 'display',
                    'columns', 'aliases'),
                [Column(table, 'asdf', type=str)]))

    def test_foreign_key_or_column(self):
        """Tests the utils.foreign_key_or_column function"""

        con = DbTestCase.connection
        user = con.table('user')
        article = con.table('article')

        self.assertEqual(
            user.column('id'),
            utils.foreign_key_or_column(user, 'id')
        )
        self.assertEqual(
            article.foreign_key('user_id'),
            utils.foreign_key_or_column(article, 'user_id')
        )
        self.assertEqual(
            None,
            utils.foreign_key_or_column(article, 'foo')
        )

    def test_unicode_decode(self):
        """Tests the utils.unicode_decode function"""

        self.assertEqual(
            u'3.14',
            utils.unicode_decode(3.14)
        )

    def test_filter_keys(self):
        """Tests the utils.filter_keys function"""

        self.assertEqual(
            {'a': 1, 'b': 2},
            utils.filter_keys({'a': 1, 'b': 2, 'c': 3}, 'a', 'b')
        )
        self.assertEqual(
            {},
            utils.filter_keys({'a': 1, 'b': 2, 'c': 3}, 'd', 'e')
        )

    def test_freeze(self):
        """Tests the utils.freeze function"""

        self.assertEqual(
            ('a', 'b'),
            utils.freeze(['a', 'b'])
        )
