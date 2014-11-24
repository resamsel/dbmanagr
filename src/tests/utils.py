#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest

from tests.testcase import ParentTestCase
from dbnav import utils
from dbnav.model.column import Column
from dbnav.comment import Comment


def load_suite():
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromTestCase(UtilsTestCase)
    return suite


class UtilsTestCase(ParentTestCase):
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

        self.assertEqual(
            None,
            utils.create_title(None, []))
        self.assertEqual(
            ('name', '{name}'),
            utils.create_title(None, [Column(None, 'name', type=str)]))
        self.assertEqual(
            ('my_name', '{my_name}'),
            utils.create_title(None, [Column(None, 'my_name', type=str)]))
        self.assertEqual(
            ('asdf', '{asdf}'),
            utils.create_title(None, [Column(None, 'asdf', type=str)]))
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
                [Column(None, 'asdf', type=str)]))
