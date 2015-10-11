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

from dbmanagr.dto import Dto
from dbmanagr.jsonable import from_json
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


class BaseNode(Dto):
    def __eq__(self, o):
        return hash(self) == hash(o)

    def __hash__(self):
        return hash(str(self))

    def format(self):
        return Formatter.format_node(self)

    def format_verbose(self, verbosity=0):
        if verbosity > -1:
            return self.format()
        return None


class ColumnNode(BaseNode):
    def __init__(self, column, indent=0):
        BaseNode.__init__(self)

        self.column = column
        self.indent = indent

    def __hash__(self):
        return hash(str(self.column))

    def __str__(self):
        indent = '  ' * self.indent
        return '{0}- {1}{2}{3}'.format(
            indent,
            self.column.name,
            PRIMARY_KEY_OPTIONS.get(self.column.primary_key),
            NULLABLE_OPTIONS.get(self.column.nullable))

    def format(self):
        return Formatter.format_column_node(self)

    def format_verbose(self, verbosity=0):
        indent = '  ' * self.indent
        return '{0}- {1}'.format(indent, self.column.ddl())

    @staticmethod
    def from_json(d):
        return ColumnNode(from_json(d['column']), from_json(d['indent']))


class ForeignKeyNode(BaseNode):
    def __init__(self, fk, parent=None, indent=0):
        BaseNode.__init__(self)

        self.fk = fk
        self.parent = parent
        self.indent = indent

    def __str__(self):
        indent = '  ' * self.indent
        if self.fk.a.tablename == self.parent.name:
            return u'{0}→ {1}{3} → {2}'.format(
                indent,
                self.fk.a.name,
                self.fk.b,
                NULLABLE_OPTIONS.get(self.fk.a.nullable))
        return u'{0}↑ {1} ({2} → {3}.{4})'.format(
            indent,
            self.fk.a.tablename,
            self.fk.a.name,
            self.fk.b.tablename,
            self.fk.b.name)

    def __hash__(self):
        return hash(str(self.fk))

    def format(self):
        return Formatter.format_foreign_key_node(self)

    @staticmethod
    def from_json(d):
        return ForeignKeyNode(
            from_json(d['fk']),
            from_json(d['parent']),
            from_json(d['indent'])
        )


class TableNode(BaseNode):
    def __init__(self, table, indent=0):
        BaseNode.__init__(self)

        self.table = table
        self.indent = indent

    def __str__(self):
        return self.table.name

    def __hash__(self):
        return hash(str(self.table))

    def format(self):
        return Formatter.format_table_node(self)

    @staticmethod
    def from_json(d):
        return TableNode(
            from_json(d['table']),
            from_json(d['indent'])
        )


class NameNode(BaseNode):
    def __init__(self, name, indent=0):
        BaseNode.__init__(self)

        self.name = name
        self.indent = indent

    def __str__(self):
        return '{0}{1}'.format('  ' * self.indent, self.name)

    def __hash__(self):
        return hash(self.name)

    def format(self):
        return Formatter.format_name_node(self)

    @staticmethod
    def from_json(d):
        return NameNode(
            from_json(d['name']),
            from_json(d['indent'])
        )
