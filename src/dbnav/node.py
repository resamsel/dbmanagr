#!/usr/bin/env python
# -*- coding: utf-8 -*-

from dbnav.formatter import Formatter

PRIMARY_KEY_OPTIONS = {
    True: '*',
    False: ''
}
NULLABLE_OPTIONS = {
    True: '?',
    False: '',
    None: ''
}

class BaseNode:
    def __hash__(self):
        return hash(self.__dict__)
    def __eq__(self, o):
        return hash(self) == hash(o)
    def format(self):
        return Formatter.format_node(self)

class ColumnNode(BaseNode):
    def __init__(self, column, indent=0):
        self.column = column
        self.indent = indent
    def __hash__(self):
        return hash(str(self.column))
    def __str__(self):
        indent = '  '*self.indent
        return '{0}- {1}{2}{3}'.format(indent,
            self.column.name,
            PRIMARY_KEY_OPTIONS.get(self.column.primary_key),
            NULLABLE_OPTIONS.get(self.column.nullable),
            self.column.table.name)
    def format(self):
        return Formatter.format_column_node(self)

class ForeignKeyNode(BaseNode):
    def __init__(self, fk, parent=None, indent=0):
        self.fk = fk
        self.parent = parent
        self.indent = indent
    def escaped(self, f):
        return dict(map(lambda (k, v): (k.encode('ascii', 'ignore'), f(v)), self.__dict__.iteritems()))
    def __getattr__(self, name):
        if self.fk:
            return getattr(self.fk, name)
        if name in self.__dict__:
            return self.__dict__[name]
        return None
    def __hash__(self):
        return hash(str(self.fk))
    def __repr__(self):
        return self.__str__()
    def __str__(self):
        indent = '  '*self.indent
        if self.fk.a.table.name == self.parent.name:
            return u'{0}→ {1}{3} → {2}'.format(indent,
                self.fk.a.name,
                self.fk.b,
                NULLABLE_OPTIONS.get(self.fk.a.nullable))
        return u'{0}↑ {1} ({2} → {3}.{4})'.format(indent,
            self.fk.a.table.name, self.fk.a.name, self.fk.b.table.name, self.fk.b.name)
    def format(self):
        return Formatter.format_foreign_key_node(self)

class TableNode(BaseNode):
    def __init__(self, table, include=[], exclude=[], indent=0):
        self.table = table
        self.include = include
        self.exclude = exclude
        self.indent = indent
    def __hash__(self):
        return hash(self.table.autocomplete())
    def __str__(self):
        return self.table.name
    def format(self):
        return Formatter.format_table_node(self)

class NameNode(BaseNode):
    def __init__(self, name, indent=0):
        self.name = name
        self.indent = indent
    def __hash__(self):
        return hash(self.name)
    def __str__(self):
        return '{0}{1}'.format('  '*self.indent, self.name)
    def format(self):
        return Formatter.format_name_node(self)