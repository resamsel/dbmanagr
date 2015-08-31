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
from dbnav.command.grapher import node


class NodeTestCase(ParentTestCase):
    def test_column_node_hash(self):
        """Tests the node.ColumnNode __hash__ method"""

        self.assertEqual(
            hash(str('a')),
            node.ColumnNode('a').__hash__()
        )

    def test_base_node_eq(self):
        """Tests the node.BaseNode __eq__ method"""

        self.assertEqual(node.ColumnNode('a'), node.ColumnNode('a'))

    def test_table_node(self):
        """Tests the node.TableNode class"""

        from dbnav.model.table import Table
        table = Table(name='a')

        self.assertEqual(node.TableNode(table), node.TableNode(table))

    def test_name_node(self):
        """Tests the node.NameNode class"""

        self.assertEqual(node.NameNode('a'), node.NameNode('a'))
        self.assertEqual('# root element\na:', node.NameNode('a').format())

    def test_foreign_key_node_hash(self):
        """Tests the node.ForeignKeyNode __hash__ method"""

        self.assertEqual(
            hash(str({'a': 'b'})),
            node.ForeignKeyNode({'a': 'b'}).__hash__()
        )

    def test_foreign_key_node_getattr(self):
        """Tests the node.ForeignKeyNode __getattr__ method"""

        self.assertEqual(
            'A',
            node.ForeignKeyNode('a').capitalize()
        )
