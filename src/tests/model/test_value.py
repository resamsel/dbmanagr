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

from tests.testcase import ParentTestCase
from dbmanagr.model import value


class ValueTestCase(ParentTestCase):
    def test_title(self):
        """Tests the Value.title method"""

        self.assertEqual(
            '[BLOB]',
            value.Value(
                memoryview(b'Blob'), None, None, True, None).title())

    def test_as_json(self):
        """Tests the Value.as_json method"""

        v = value.Value('a', 'b', None, None, None)

        self.assertEqual(
            {
                '__cls__': "<class 'dbmanagr.model.value.Value'>",
                'value': 'a',
                'subtitle': 'b'
            },
            v.as_json()
        )
