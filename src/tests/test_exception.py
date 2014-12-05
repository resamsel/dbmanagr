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