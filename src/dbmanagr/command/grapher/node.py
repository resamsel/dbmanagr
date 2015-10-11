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

from dbmanagr.jsonable import Jsonable
from dbmanagr.formatter import Formatter

PRIMARY_KEY_OPTIONS = {
    True: '*',
    False: ''
}
NULLABLE_OPTIONS = {
    True: '?',
    False: '',
    None: ''
}


class BaseNode(Jsonable):
    def __eq__(self, o):
        return hash(self) == hash(o)


class ColumnNode(BaseNode):
    def __init__(self, column, indent=0):
        self.column = column
        self.indent = indent

    def __hash__(self):
        return hash(str(self.column))


class ForeignKeyNode(BaseNode):
    def __init__(self, fk, parent=None, indent=0):
        self.fk = fk
        self.parent = parent
        self.indent = indent

    def __getattr__(self, name):
        return getattr(self.fk, name)

    def __hash__(self):
        return hash(str(self.fk))


class TableNode(BaseNode):
    def __init__(self, table, include=None, exclude=None, indent=0):
        if include is None:
            include = {}
        if exclude is None:
            exclude = {}

        self.table = table
        self.include = include
        self.exclude = exclude
        self.indent = indent

    def __hash__(self):
        return hash(self.table.autocomplete())


class NameNode(BaseNode):
    def __init__(self, name, indent=0):
        self.name = name
        self.indent = indent

    def __hash__(self):
        return hash(self.name)

    def __str__(self):
        return '{0}{1}'.format('  ' * self.indent, self.name)

    def format(self):
        return Formatter.format_name_node(self)
