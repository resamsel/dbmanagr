#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import codecs
import sys

UTF8Writer = codecs.getwriter('utf8')
sys.stdout = UTF8Writer(sys.stdout)

def html_escape(s):
    if type(s) == str or type(s) == unicode:
        return s.replace('&', '&amp;').replace('"', '&quot;').replace('<', '&lt;')
    return s

class DefaultWriter:
    def write(self, items):
        s = self.str(items)
        print s
        return s
    def str(self, items):
        return map(lambda item: self.itemtostring(item), items)
    def itemtostring(self, item):
        return str(item)

class XmlWriter(DefaultWriter):
    ITEMS_FORMAT = u"""<items>
{0}</items>"""
    ITEM_FORMAT = u"""   <item uid="{uid}" arg="{title}" autocomplete="{autocomplete}" valid="{valid}">
        <title>{title}</title>
        <subtitle>{subtitle}</subtitle>
        <icon>{icon}</icon>
    </item>
"""
    def str(self, items):
        s = ''.join([self.itemtostring(i) for i in items])
        return XmlWriter.ITEMS_FORMAT.format(s)
    def itemtostring(self, item):
        return XmlWriter.ITEM_FORMAT.format(**item.escaped(html_escape))


class JsonWriter(DefaultWriter):
    ITEMS_FORMAT = u"""{{
{0}}}"""
    ITEM_FORMAT = u"""   {{ "uid": "{uid}", "arg": "{title}", "autocomplete": "{autocomplete}", "valid": "{valid}", "title": "{title}", "subtitle": "{subtitle}", "icon": "{icon}" }}
"""
    def str(self, items):
        s = ''.join([self.itemtostring(i) for i in items])
        return JsonWriter.ITEMS_FORMAT.format(s)
    def itemtostring(self, item):
        return JsonWriter.ITEM_FORMAT.format(**item.escaped(html_escape))

class SimpleWriter(DefaultWriter):
    ITEMS_FORMAT = u"""Id\tTitle\tSubtitle\tAutocomplete
{0}"""
    ITEM_FORMAT = u"""{uid}\t{title}\t{subtitle}\t{autocomplete}
"""
    def str(self, items):
        s = u''.join([self.itemtostring(i) for i in items])
        return SimpleWriter.ITEMS_FORMAT.format(s)
    def itemtostring(self, item):
        return SimpleWriter.ITEM_FORMAT.format(**item.escaped(html_escape))

class StdoutWriter(DefaultWriter):
    ITEMS_FORMAT = u"""Title\tSubtitle\tAutocomplete
{0}"""
    ITEM_FORMAT = u"""{title}\t{subtitle}\t{autocomplete}
"""
    def str(self, items):
        s = u''.join([self.itemtostring(i) for i in items])
        return StdoutWriter.ITEMS_FORMAT.format(s)
    def itemtostring(self, item):
        return StdoutWriter.ITEM_FORMAT.format(**item.escaped(html_escape))

class AutocompleteWriter(DefaultWriter):
    ITEMS_FORMAT = u"""{0}"""
    ITEM_FORMAT = u"""{autocomplete}
"""
    def str(self, items):
        s = u''.join([self.itemtostring(i) for i in items])
        return AutocompleteWriter.ITEMS_FORMAT.format(s)
    def itemtostring(self, item):
        return AutocompleteWriter.ITEM_FORMAT.format(**item.escaped(html_escape))

class StringWriter(SimpleWriter):
    def write(self, items):
        return self.str(items)

class Writer:
    writer = StdoutWriter()

    @staticmethod
    def set(arg):
        Writer.writer = arg

    @staticmethod
    def write(items):
        return Writer.writer.write(items)
