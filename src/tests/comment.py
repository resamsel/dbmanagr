#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest

from collections import Counter

from tests.testcase import ParentTestCase
from dbnav.model.column import Column
from dbnav import comment
from tests.mock.data import FOREIGN_KEYS


def load_suite():
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromTestCase(CommentTestCase)
    return suite


class CommentTestCase(ParentTestCase):
    def test_update_aliases(self):
        """Tests the utils.update_aliases function"""

        self.assertEqual(
            {},
            comment.update_aliases(None, None, {}, {}))
        self.assertEqual(
            {'t2': '_t2', 't3': '_t3'},
            comment.update_aliases('t1', Counter(), {}, FOREIGN_KEYS))
        self.assertEqual(
            {'t4': '_t4'},
            comment.update_aliases('t2', Counter(), {}, FOREIGN_KEYS))
        self.assertEqual(
            {},
            comment.update_aliases('t3', Counter(), {}, FOREIGN_KEYS))

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
