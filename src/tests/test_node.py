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
from dbnav import node


class NodeTestCase(ParentTestCase):
    def test_format(self):
        """Tests the node.BaseNode format method"""

        self.assertIsNotNone(
            node.BaseNode().format()
        )

    def test_format_verbose(self):
        """Tests the node.BaseNode format_verbose method"""

        self.assertIsNotNone(
            node.BaseNode().format_verbose()
        )

    def test_column_node_hash(self):
        """Tests the node.ColumnNode __hash__ method"""

        self.assertEqual(
            hash(str('a')),
            node.ColumnNode('a').__hash__()
        )