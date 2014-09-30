#!/usr/bin/env python
# -*- coding: utf-8 -*-

from dbnav.writer import FormatWriter
from dbnav.formatter import Formatter, DefaultFormatter

class SqlInsertWriter(FormatWriter):
    def __init__(self):
        FormatWriter.__init__(self, u'{0}', u'insert into {table} ({columns}) values ({values});')
        Formatter.set(DefaultFormatter())
    def itemtostring(self, item):
        row = item.row
        exclude = item.exclude
        table = row.table
        return self.item_format.format(
            table=table.connection.escape_keyword(table.name),
            columns=self.create_columns(row, exclude),
            values=self.create_values(row, exclude))
    def create_columns(self, row, exclude):
        return u','.join(
            map(lambda col: col.name,
                filter(lambda col: col.name not in exclude, row.table.cols)))
    def create_values(self, row, exclude):
        table = row.table
        return u','.join(
            map(lambda col: table.connection.format_value(col, row[col.name]),
                 filter(lambda col: col.name not in exclude, table.cols)))

class SqlUpdateWriter(FormatWriter):
    def __init__(self):
        FormatWriter.__init__(self, u'{0}', u'update {table} set {values} where {restriction};')
        Formatter.set(DefaultFormatter())
    def itemtostring(self, item):
        row = item.row
        exclude = item.exclude
        table = row.table
        return self.item_format.format(
            table=table.connection.escape_keyword(table.name),
            values=self.create_values(row, exclude),
            restriction=self.create_restriction(row,
                filter(lambda col: col.primary_key, table.cols)))
    def create_values(self, row, exclude):
        table = row.table
        return u', '.join(
            map(lambda col: table.connection.restriction(
                        None, col, '=', row[col.name], map_null_operator=False),
                filter(lambda col: not col.primary_key and col.name not in exclude,
                    row.table.cols)))
    def create_restriction(self, row, pks):
        table = row.table
        return u' and '.join(
            map(lambda col: table.connection.restriction(None, col, '=', row[col.name]),
                 pks))

class SqlDeleteWriter(FormatWriter):
    def __init__(self):
        FormatWriter.__init__(self, u'{0}', u'delete from {table} where {restriction};')
        Formatter.set(DefaultFormatter())
    def itemtostring(self, item):
        row = item.row
        exclude = item.exclude
        table = row.table
        return self.item_format.format(
            table=table.connection.escape_keyword(table.name),
            restriction=self.create_restriction(row,
                filter(lambda col: col.primary_key, table.cols)))
    def create_restriction(self, row, pks):
        table = row.table
        return u' and '.join(
            map(lambda col: table.connection.restriction(None, col, '=', row[col.name]),
                 pks))

class YamlWriter(FormatWriter):
    def __init__(self):
        FormatWriter.__init__(self, u'{0}', u"""{prefix}    - &{table}_{id} !!models.{table}
        {columns}""")
        Formatter.set(DefaultFormatter())
        self.last_table = None
    def itemtostring(self, item):
        row = item.row
        exclude = item.exclude
        table = row.table
        prefix = ''
        if self.last_table != table:
            prefix = u"""
{0}s:
""".format(table)
            self.last_table = table
        return self.item_format.format(
            table=table.connection.escape_keyword(table.name),
            id=row[0],
            prefix=prefix,
            columns=self.create_columns(row, exclude),
            values=self.create_values(row, exclude))
    def create_columns(self, row, exclude):
        table = row.table
        return u"""
        """.join(
            map(lambda col: '{0}: {1}'.format(col.name, row[col.name]),
                filter(lambda col: col.name not in exclude, row.table.cols)))
    def create_values(self, row, exclude):
        table = row.table
        return u','.join(
            map(lambda col: table.connection.format_value(col, row[col.name]),
                 filter(lambda col: col.name not in exclude, table.cols)))

