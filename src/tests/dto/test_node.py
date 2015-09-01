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
from dbnav.dto import node


class BaseNodeTestCase(ParentTestCase):
    def test_hash(self):
        """Tests the BaseNode.__hash__ method"""

        n = node.BaseNode()

        self.assertEqual(hash(n), n.__hash__())

    def test_format(self):
        """Tests the BaseNode.format method"""

        n = node.BaseNode()

        self.assertIsNotNone(n.format())

    def test_format_verbose(self):
        """Tests the BaseNode.format_verbose method"""

        n = node.BaseNode()

        self.assertIsNotNone(n.format_verbose())
        self.assertIsNone(n.format_verbose(-1))


class ColumnNodeTestCase(ParentTestCase):
    def test_hash(self):
        """Tests the ColumnNode.__hash__ method"""

        n = node.ColumnNode('a')

        self.assertEqual(hash(n), n.__hash__())

    def test_from_json(self):
        """Tests the ColumnNode.from_json static method"""

        n = node.ColumnNode(None)

        self.assertEqual(
            n,
            node.ColumnNode.from_json({
                'column': None,
                'indent': 0
            })
        )


class ForeignKeyNodeTestCase(ParentTestCase):
    def test_hash(self):
        """Tests the ForeignKeyNode.__hash__ method"""

        n = node.ForeignKeyNode('a')

        self.assertEqual(hash(n), n.__hash__())

    def test_from_json(self):
        """Tests the ForeignKeyNode.from_json static method"""

        n = node.ForeignKeyNode(None)

        self.assertEqual(
            n,
            node.ForeignKeyNode.from_json({
                'fk': None,
                'parent': None,
                'indent': 0
            })
        )


class TableNodeTestCase(ParentTestCase):
    def test_hash(self):
        """Tests the TableNode.__hash__ method"""

        n = node.TableNode('a')

        self.assertEqual(hash(n), n.__hash__())

    def test_from_json(self):
        """Tests the TableNode.from_json static method"""

        n = node.TableNode(None)

        self.assertEqual(
            n,
            node.TableNode.from_json({
                'table': None,
                'indent': 0
            })
        )
