#!/usr/bin/env python
# -*- coding: utf-8 -*-

from dbnav.writer import FormatWriter, StdoutWriter
from dbnav.formatter import Formatter, DefaultFormatter
import datetime

import pprint
pp = pprint.PrettyPrinter(indent=4)

def sql_escape(value):
    if type(value) is str or type(value) is unicode:
        return "'%s'" % value
    if type(value) in [datetime.datetime, datetime.date, datetime.time]:
        return "'%s'" % value
    if type(value) is bool:
        return unicode(value).lower()
    return unicode(value)

class ExecuteWriter(StdoutWriter):
    def __init__(self, options=None):
        StdoutWriter.__init__(self, u'{0}', u'{item}')
        Formatter.set(DefaultFormatter())

class SqlInsertWriter(FormatWriter):
    def __init__(self, options=None):
        FormatWriter.__init__(self, u'{0}', u'insert into {table} ({columns}) values ({values});')
        Formatter.set(DefaultFormatter())
        self.table_name = options.table_name
    def itemtostring(self, item):
        row = item.row
        return self.item_format.format(
            table=self.table_name,
            columns=self.create_columns(row.keys()),
            values=self.create_values(row.values()))
    def create_columns(self, cols):
        return u','.join(map(unicode, cols))
    def create_values(self, values):
        return u','.join(map(sql_escape, values))

class ExecuteTestWriter(ExecuteWriter):
    pass
