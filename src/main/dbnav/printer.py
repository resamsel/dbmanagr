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

class DefaultPrinter:
    def write(self, items):
        print map(lambda item: self.itemtostring(item), items)
    def itemtostring(self, item):
        return str(item)

class XmlPrinter(DefaultPrinter):
    ITEMS_FORMAT = u"""<items>
{0}</items>"""
    ITEM_FORMAT = u"""   <item uid="{uid}" arg="{title}" autocomplete="{autocomplete}" valid="{valid}">
        <title>{title}</title>
        <subtitle>{subtitle}</subtitle>
        <icon>{icon}</icon>
    </item>
"""
    def write(self, items):
        s = ''.join([self.itemtostring(i) for i in items])
        print XmlPrinter.ITEMS_FORMAT.format(s)
    def itemtostring(self, item):
        return XmlPrinter.ITEM_FORMAT.format(**item.escaped(html_escape))


class JsonPrinter(DefaultPrinter):
    ITEMS_FORMAT = u"""{{
{0}}}"""
    ITEM_FORMAT = u"""   {{ "uid": "{uid}", "arg": "{title}", "autocomplete": "{autocomplete}", "valid": "{valid}", "title": "{title}", "subtitle": "{subtitle}", "icon": "{icon}" }}
"""
    def write(self, items):
        s = ''.join([self.itemtostring(i) for i in items])
        print JsonPrinter.ITEMS_FORMAT.format(s)
    def itemtostring(self, item):
        return JsonPrinter.ITEM_FORMAT.format(**item.escaped(html_escape))

class SimplePrinter(DefaultPrinter):
    ITEMS_FORMAT = u"""Id\tTitle\tSubtitle\tAutocomplete
{0}"""
    ITEM_FORMAT = u"""{uid}\t{title}\t{subtitle}\t{autocomplete}
"""
    def write(self, items):
        s = u''.join([self.itemtostring(i) for i in items])
        print SimplePrinter.ITEMS_FORMAT.format(s)
    def itemtostring(self, item):
        return SimplePrinter.ITEM_FORMAT.format(**item.escaped(html_escape))

class StdoutPrinter(DefaultPrinter):
    ITEMS_FORMAT = u"""Title\tSubtitle\tAutocomplete
{0}"""
    ITEM_FORMAT = u"""{title}\t{subtitle}\t{autocomplete}
"""
    def write(self, items):
        s = u''.join([self.itemtostring(i) for i in items])
        print StdoutPrinter.ITEMS_FORMAT.format(s)
    def itemtostring(self, item):
        return StdoutPrinter.ITEM_FORMAT.format(**item.escaped(html_escape))

class AutocompletePrinter(DefaultPrinter):
    ITEMS_FORMAT = u"""{0}"""
    ITEM_FORMAT = u"""{autocomplete} """
    def write(self, items):
        s = u''.join([self.itemtostring(i) for i in items])
        print AutocompletePrinter.ITEMS_FORMAT.format(s)
    def itemtostring(self, item):
        return AutocompletePrinter.ITEM_FORMAT.format(**item.escaped(html_escape))

class Printer:
    printer = StdoutPrinter()

    @staticmethod
    def set(arg):
        Printer.printer = arg

    @staticmethod
    def write(items):
        Printer.printer.write(items)
