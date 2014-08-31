#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import codecs
import sys

from collections import OrderedDict
from dbnav.item import Item
from dbnav.node import ColumnNode
from dbnav.formatter import Formatter, XmlFormatter, SimplifiedFormatter, TestFormatter, GraphvizFormatter, DefaultFormatter

UTF8Writer = codecs.getwriter('utf8')
sys.stdout = UTF8Writer(sys.stdout)

def html_escape(s):
    if type(s) == str or type(s) == unicode:
        return s.replace('&', '&amp;').replace('"', '&quot;').replace('<', '&lt;')
    return s

def escape(s):
    if type(s) == unicode:
        return s.replace('"', '&quot;')
    return s

class DefaultWriter:
    def write(self, items):
        return self.str(items)
    def str(self, items):
        return map(lambda item: self.itemtostring(item), items)
    def itemtostring(self, item):
        return unicode(item)

class StdoutWriter(DefaultWriter):
    def __init__(self,
            items_format=u"""Title\tSubtitle\tAutocomplete
{0}""",
            item_format=u"""{title}\t{subtitle}\t{autocomplete}""",
            item_separator=u"""
""",
            format_error_format=u'{0}'):
        self.items_format = items_format
        self.item_format = item_format
        self.item_separator = item_separator
        self.format_error_format = format_error_format
        
        Formatter.set(DefaultFormatter())
    def filter(self, items):
        return items
    def str(self, items):
        s = self.item_separator.join(
            map(lambda i: self.itemtostring(i),
                self.filter(items)))
        return self.items_format.format(s)
    def itemtostring(self, item):
        if hasattr(item, '__dict__'):
            try:
                return self.item_format.format(item=unicode(item), **item.__dict__)
            except:
                raise
                return self.format_error_format.format(item=item, **item.__dict__)
        return self.item_format.format(item=item)

class AutocompleteWriter(StdoutWriter):
    def __init__(self):
        StdoutWriter.__init__(self, u'{0}', u'{autocomplete}')

class SimpleWriter(StdoutWriter):
    def __init__(self):
        StdoutWriter.__init__(self,
            u"""Id\tTitle\tSubtitle\tAutocomplete
{0}""",
            u"""{uid}\t{title}\t{subtitle}\t{autocomplete}""")

class JsonWriter(StdoutWriter):
    def __init__(self):
        StdoutWriter.__init__(self,
            u"""{{
{0}}}""",
            u"""   {{ "uid": "{uid}", "arg": "{title}", "autocomplete": "{autocomplete}", "valid": "{valid}", "title": "{title}", "subtitle": "{subtitle}", "icon": "{icon}" }}""")

class StringWriter(SimpleWriter):
    def write(self, items):
        return self.str(items)

class FormatWriter(StdoutWriter):
    def __init__(self,
            items_format=u"""Title\tSubtitle\tAutocomplete
{0}""",
            item_format=u"""{title}\t{subtitle}\t{autocomplete}""",
            item_separator=u"""
""",
            format_error_format=u'{0}'):
        StdoutWriter.__init__(self, items_format, item_format, item_separator, format_error_format)
    def itemtostring(self, item):
        return item.format()

class SimplifiedWriter(FormatWriter):
    def __init__(self):
        FormatWriter.__init__(self, u'{0}')
        Formatter.set(SimplifiedFormatter())

class XmlWriter(FormatWriter):
    def __init__(self):
        FormatWriter.__init__(self,
            u"""<items>
{0}
</items>""")
        Formatter.set(XmlFormatter())
    def write(self, items):
        if not items:
            items = [Item(None, 'Nothing found', '', '', 'no', 'images/icon.png')]
        return self.str(items)

class GraphvizWriter(FormatWriter):
    def __init__(self):
        FormatWriter.__init__(self, u"""digraph dbgraph {{
{0}
}}""")
        Formatter.set(GraphvizFormatter())
    def filter(self, items):
        # Removes duplicate items and keeps order
        return list(OrderedDict.fromkeys(
            filter(lambda i: not isinstance(i, ColumnNode), items)))

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
            restriction=self.create_restriction(row, exclude))
    def create_values(self, row, exclude):
        table = row.table
        return u', '.join(
            map(lambda col: table.connection.restriction(None, col, '=', row[col.name]),
                filter(lambda col: col.name not in exclude, row.table.cols)))
    def create_restriction(self, row, exclude):
        table = row.table
        return u' and '.join(
            map(lambda col: table.connection.restriction(None, col, '=', row[col.name]),
                 filter(lambda col: col.primary_key, table.cols)))

class TestWriter(FormatWriter):
    def __init__(self, items_format=u"""Title\tAutocomplete
{0}""",
            item_format=u"""{title}\t{autocomplete}"""):
        FormatWriter.__init__(self, items_format, item_format)
        Formatter.set(TestFormatter())

class Writer:
    writer = StdoutWriter()

    @staticmethod
    def set(arg):
        Writer.writer = arg
    
    @staticmethod
    def from_options(options):
        if options.default: Writer.set(DefaultWriter())
        if options.simple: Writer.set(SimpleWriter())
        if options.json: Writer.set(JsonWriter())
        if options.xml: Writer.set(XmlWriter())
        if options.autocomplete: Writer.set(AutocompleteWriter())
        if options.test: Writer.set(TestWriter())

    @staticmethod
    def write(items):
        return Writer.writer.write(items)
