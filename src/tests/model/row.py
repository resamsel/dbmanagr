#!/usr/bin/env python
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

from collections import OrderedDict

from tests.testcase import DbTestCase
from dbnav.model import row


def load_suite():
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromTestCase(RowTestCase)
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


class RowTestCase(DbTestCase):
    def test_val(self):
        """Tests the row.foreign_key_or_column function"""

        con = DbTestCase.connection
        user = con.table('user')
        r = row.Row(
            user, ResultRow(OrderedDict([('id', 1), ('foo', 'Bar')])))

        self.assertEqual(
            None, row.val(r, 'bar'))
        self.assertEqual(
            1, row.val(r, 'id'))
        self.assertEqual(
            'Bar', row.val(r, 'foo'))
        self.assertEqual(
            'Bar', r['foo'])
        self.assertEqual(
            None, r['bar'])
        self.assertEqual(
            'Bar', row.val(r, 1))
