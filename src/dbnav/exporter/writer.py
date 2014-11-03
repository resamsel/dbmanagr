#!/usr/bin/env python
# -*- coding: utf-8 -*-

from string import capwords

from dbnav.writer import FormatWriter
from dbnav.formatter import Formatter, DefaultFormatter

class SqlInsertWriter(FormatWriter):
    def __init__(self, options=None):
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
                filter(lambda col: col.name not in exclude, row.table.columns())))
    def create_values(self, row, exclude):
        table = row.table
        return u','.join(
            map(lambda col: table.connection.format_value(col, row[col.name]),
                 filter(lambda col: col.name not in exclude, table.columns())))

class SqlUpdateWriter(FormatWriter):
    def __init__(self, options=None):
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
                filter(lambda col: col.primary_key, table.columns())))
    def create_values(self, row, exclude):
        table = row.table
        return u', '.join(
            map(lambda col: table.connection.restriction(
                        None, col, '=', row[col.name], map_null_operator=False),
                filter(lambda col: not col.primary_key and col.name not in exclude,
                    row.table.columns())))
    def create_restriction(self, row, pks):
        table = row.table
        return u' and '.join(
            map(lambda col: table.connection.restriction(None, col, '=', row[col.name]),
                 pks))

class SqlDeleteWriter(FormatWriter):
    def __init__(self, options=None):
        FormatWriter.__init__(self, u'{0}', u'delete from {table} where {restriction};')
        Formatter.set(DefaultFormatter())
    def itemtostring(self, item):
        row = item.row
        exclude = item.exclude
        table = row.table
        return self.item_format.format(
            table=table.connection.escape_keyword(table.name),
            restriction=self.create_restriction(row,
                filter(lambda col: col.primary_key, table.columns())))
    def create_restriction(self, row, pks):
        table = row.table
        return u' and '.join(
            map(lambda col: table.connection.restriction(None, col, '=', row[col.name]),
                 pks))

def yaml_format_entity(name):
    return capwords(name, '_').replace('_', '')

def yaml_format_field(name):
    s = yaml_format_entity(name)
    return s[:1].lower() + s[1:]

def yaml_field(col):
    if col.name in col.table.fks:
        fk = col.table.fks[col.name]
        return yaml_format_field(fk.b.table.name)
    return yaml_format_field(col.name)

def yaml_value(col, value):
    if col.name in col.table.fks:
        fk = col.table.fks[col.name]
        return u'*{table}_{id}'.format(table=fk.b.table.name.replace('_',''), id=yaml_value(fk.b, value))
    if value is None:
        return u'!!null null'
    if type(value) is float:
        return u'!!float %f' % value
    if type(value) is int:
        return u'!!int %d' % value
    if type(value) is bool:
        return u'!!bool %s' % unicode(value).lower()
    return value

class YamlWriter(FormatWriter):
    def __init__(self, options=None):
        FormatWriter.__init__(self, u'{0}', u"""{prefix}    - &{table}_{id} !!{package}.{model}
        {tuples}""")
        Formatter.set(DefaultFormatter())
        self.package = options.package
        self.last_table = None
    def itemtostring(self, item):
        row = item.row
        exclude = item.exclude
        table = row.table
        tablename = table.connection.escape_keyword(table.name).replace('_','')
        prefix = ''
        if self.last_table != table:
            if self.last_table:
                prefix = u"""
{0}s:
""".format(tablename)
            else:
                prefix = u"""{0}s:
""".format(tablename)
            self.last_table = table
        return self.item_format.format(
            table=tablename,
            id=row[0],
            prefix=prefix,
            package=self.package,
            model=yaml_format_entity(table.name),
            tuples=self.create_tuples(row, exclude))
    def create_tuples(self, row, exclude):
        table = row.table
        return u"""
        """.join(
            map(lambda col: '{0}: {1}'.format(yaml_field(col), yaml_value(col, row[col.name])),
                filter(lambda col: col.name not in exclude, row.table.columns())))

