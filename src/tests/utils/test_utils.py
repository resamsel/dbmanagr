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
            (None, None),
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

    def test_to_dict(self):
        """Tests the utils.to_dict function"""

        self.assertEqual({}, utils.to_dict(None, {}))
        self.assertEqual({}, utils.to_dict([], {}))

        self.assertEqual(
            {'a': None},
            utils.to_dict(['a.'], {})
        )
        self.assertEqual(
            {'a': None, 'b': None},
            utils.to_dict(['a', 'b'], {})
        )
        self.assertEqual(
            {'a': {'b': None, 'c': None}, 'd': None, 'e': {'f': {'g': None}}},
            utils.to_dict(['a.b', 'a.c', 'd', 'e.f.g'], {})
        )
        self.assertEqual(
            {'a': {'b': '1', 'c': None}, 'd': None, 'e': {'f': {'g': None}}},
            utils.to_dict(['a.b=1', 'a.c', 'd', 'e.f.g'], {})
        )

    def test_is_included(self):
        """Tests the utils.is_included function"""

        d = {
            'a': {
                'b': False,
                'c': None
            },
            'd': None,
            'e': {
                'f': {
                    'g': None
                }
            }
        }

        self.assertEqual(False, utils.is_included('a', {}))
        self.assertEqual(True, utils.is_included('a', None))

        self.assertEqual(True, utils.is_included('a', d))
        self.assertEqual(False, utils.is_included('b', d))
        self.assertEqual(False, utils.is_included('c', d))
        self.assertEqual(True, utils.is_included('d', d))
        self.assertEqual(True, utils.is_included('e', d))
        self.assertEqual(False, utils.is_included('f', d))
        self.assertEqual(False, utils.is_included('g', d))

        self.assertEqual(False, utils.is_included('b', d['a']))
        self.assertEqual(True, utils.is_included('c', d['a']))
        self.assertEqual(True, utils.is_included('f', d['e']))
        self.assertEqual(True, utils.is_included('g', d['e']['f']))
        self.assertEqual(False, utils.is_included('g', True))
        self.assertEqual(True, utils.is_included('g', {'*': None}))

    def test_is_excluded(self):
        """Tests the utils.is_excluded function"""

        d = {
            'a': {
                'b': False,
                'c': None
            },
            'd': None,
            'e': {
                'f': {
                    'g': None
                }
            }
        }

        self.assertEqual(False, utils.is_excluded('a', {}))
        self.assertEqual(True, utils.is_excluded('a', None))

        self.assertEqual(False, utils.is_excluded('a', d))
        self.assertEqual(False, utils.is_excluded('b', d))
        self.assertEqual(False, utils.is_excluded('c', d))
        self.assertEqual(True, utils.is_excluded('d', d))
        self.assertEqual(False, utils.is_excluded('e', d))
        self.assertEqual(False, utils.is_excluded('f', d))
        self.assertEqual(False, utils.is_excluded('g', d))

        self.assertEqual(True, utils.is_excluded('b', d['a']))
        self.assertEqual(True, utils.is_excluded('c', d['a']))
        self.assertEqual(False, utils.is_excluded('f', d['e']))
        self.assertEqual(True, utils.is_excluded('g', d['e']['f']))
        self.assertEqual(True, utils.is_excluded('g', True))
        self.assertEqual(True, utils.is_excluded('g', {'*': None}))

    def test_selection(self):
        """Tests the utils.selection function"""

        d = {
            'a': {
                'b': False,
                'c': None
            },
            'd': None,
            'e': {
                'f': {
                    'g': None
                }
            }
        }

        self.assertEqual(False, utils.selection('', False))
        self.assertEqual(False, utils.selection('', {}))

        self.assertEqual(d['a'], utils.selection('a', d))
        self.assertEqual(False, utils.selection('b', d))
        self.assertEqual(False, utils.selection('c', d))
        self.assertEqual(d['d'], utils.selection('d', d))
        self.assertEqual(d['e'], utils.selection('e', d))
        self.assertEqual(False, utils.selection('f', d))
        self.assertEqual(False, utils.selection('g', d))

    def test_is_node(self):
        """Tests the utils.is_node function"""

        d = {
            'a': {
                'b': False,
                'c': None
            },
            'd': None,
            'e': {
                'f': {
                    'g': None
                }
            }
        }

        self.assertEqual(False, utils.is_node(False, ''))
        self.assertEqual(False, utils.is_node({}, ''))
        self.assertEqual(False, utils.is_node({'x': False}, 'x'))

        self.assertEqual(True, utils.is_node(d, 'a'))
        self.assertEqual(False, utils.is_node(d, 'b'))
        self.assertEqual(False, utils.is_node(d, 'c'))
        self.assertEqual(False, utils.is_node(d, 'd'))
        self.assertEqual(True, utils.is_node(d, 'e'))
        self.assertEqual(False, utils.is_node(d, 'f'))
        self.assertEqual(False, utils.is_node(d, 'g'))

    def test_to_yaml_type(self):
        """Tests the utils.to_yaml_type function"""

        from sqlalchemy.sql.sqltypes import Boolean, Integer, Float, String, \
            Date, Time, DateTime, _Binary

        self.assertEqual('str', utils.to_yaml_type(None))

        self.assertEqual('bool', utils.to_yaml_type(Boolean()))
        self.assertEqual('int', utils.to_yaml_type(Integer()))
        self.assertEqual('float', utils.to_yaml_type(Float()))
        self.assertEqual('str', utils.to_yaml_type(String()))
        self.assertEqual('str', utils.to_yaml_type(Date()))
        self.assertEqual('str', utils.to_yaml_type(Time()))
        self.assertEqual('str', utils.to_yaml_type(DateTime()))
        self.assertEqual('binary', utils.to_yaml_type(_Binary()))

    def test_to_ref(self):
        """Tests the utils.to_ref function"""

        self.assertEqual('b', utils.to_ref(None, 'b'))

        self.assertEqual('a.b', utils.to_ref('a', 'b'))

    def test_to_forward_ref(self):
        """Tests the utils.to_forward_ref function"""

        self.assertEqual('a.', utils.to_forward_ref('a'))
        self.assertEqual('a*', utils.to_forward_ref('a*'))

    def test_shell_escape(self):
        """Tests the utils.shell_escape function"""

        self.assertEqual("'*'", utils.shell_escape('*'))
        self.assertEqual("\"'*'\"", utils.shell_escape("'*'"))
        self.assertEqual('1', utils.shell_escape(1))
