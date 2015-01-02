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
from dbnav import formatter
from dbnav.node import NameNode


class FormatterTestCase(ParentTestCase):
    def test_default_formatter(self):
        """Tests the formatter.DefaultFormatter class"""

        self.assertEqual(
            'a',
            formatter.DefaultFormatter().format_item('a')
        )
        self.assertEqual(
            'a',
            formatter.DefaultFormatter().format_row(('a'))
        )
        self.assertEqual(
            'a',
            formatter.DefaultFormatter().format_node('a')
        )
        self.assertEqual(
            'a',
            formatter.DefaultFormatter().format_table_node('a')
        )

    def test_formatter(self):
        """Tests the formatter.Formatter class"""

        self.assertEqual(
            'a',
            formatter.Formatter.format_node(NameNode('a'))
        )
