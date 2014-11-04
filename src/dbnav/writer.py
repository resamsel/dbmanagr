#!/usr/bin/env python
# -*- coding: utf-8 -*-

import codecs
import sys

from dbnav.formatter import Formatter, TestFormatter, DefaultFormatter

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
        return map(self.itemtostring, items)

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
    def write(items):
        return Writer.writer.write(items)
