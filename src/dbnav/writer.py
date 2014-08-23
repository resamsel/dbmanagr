#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import codecs
import sys
from .item import Item

UTF8Writer = codecs.getwriter('utf8')
sys.stdout = UTF8Writer(sys.stdout)

def html_escape(s):
    if type(s) == str or type(s) == unicode:
        return s.replace('&', '&amp;').replace('"', '&quot;').replace('<', '&lt;')
    return s

class DefaultWriter:
    def write(self, items):
        if not items:
            items = [Item(None, 'Nothing found', '', '', 'no', 'images/icon.png')]
        s = self.str(items)
        print s
        return s
    def str(self, items):
        return map(lambda item: self.itemtostring(item), items)
    def itemtostring(self, item):
        return str(item)

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
    def str(self, items):
        s = self.item_separator.join([self.itemtostring(i) for i in items])
        return self.items_format.format(s)
    def itemtostring(self, item):
        try:
            return self.item_format.format(item=str(item), **item.__dict__)
        except:
            return self.format_error_format.format(item=item, **item.__dict__)

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

class XmlWriter(StdoutWriter):
    def __init__(self):
        StdoutWriter.__init__(self,
            u"""<items>
{0}
</items>""",
            u"""   <item uid="{uid}" arg="{value}" autocomplete="{autocomplete}" valid="{valid}">
        <title>{title}</title>
        <subtitle>{subtitle}</subtitle>
        <icon>{icon}</icon>
    </item>""")

class StringWriter(SimpleWriter):
    def write(self, items):
        return self.str(items)

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

    @staticmethod
    def write(items):
        return Writer.writer.write(items)
