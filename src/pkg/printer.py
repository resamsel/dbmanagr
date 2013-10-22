#!/usr/bin/env python
# -*- coding: utf-8 -*-

def html_escape(s):
    if type(s) == str:
        return s.replace('&', '&amp;').replace('"', '&quot;').replace('<', '&lt;')
    return s

class Printer:
    def write(self, items):
        print map(lambda item: self.itemtostring(item), items)
    def itemtostring(self, item):
        return str(item)

class XmlPrinter(Printer):
    ITEMS_FORMAT = """<items>
{0}</items>"""
    ITEM_FORMAT = """   <item uid="{uid}" arg="{title}" autocomplete="{autocomplete}" valid="{valid}">
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


class JsonPrinter(Printer):
    ITEMS_FORMAT = """{{
{0}}}"""
    ITEM_FORMAT = """   {{ "uid": "{uid}", "arg": "{title}", "autocomplete": "{autocomplete}", "valid": "{valid}", "title": "{title}", "subtitle": "{subtitle}", "icon": "{icon}" }}
"""
    def write(self, items):
        s = ''.join([self.itemtostring(i) for i in items])
        print JsonPrinter.ITEMS_FORMAT.format(s)
    def itemtostring(self, item):
        return JsonPrinter.ITEM_FORMAT.format(**item.escaped(html_escape))

class SimplePrinter(Printer):
    ITEMS_FORMAT = """Id\tTitle\tSubtitle\tAutocomplete
{0}"""
    ITEM_FORMAT = """{uid}\t{title}\t{subtitle}\t{autocomplete}
"""
    def write(self, items):
        s = ''.join([self.itemtostring(i) for i in items])
        print SimplePrinter.ITEMS_FORMAT.format(s)
    def itemtostring(self, item):
        return SimplePrinter.ITEM_FORMAT.format(**item.escaped(html_escape))
