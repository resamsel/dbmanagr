#!/usr/bin/env python
# -*- coding: utf-8 -*-

def html_escape(s):
    if type(s) == str:
        return s.replace('&', '&amp;').replace('"', '&quot;').replace('<', '&lt;')
    return s

class Printer:
    def write(self, items):
        print items

XML_ITEMS_FORMAT = """<items>
{0}</items>"""
XML_ITEM_FORMAT = """   <item uid="{0}" arg="{2}" autocomplete="{1}" valid="{5}">
        <title>{2}</title>
        <subtitle>{3}</subtitle>
        <icon>{4}</icon>
    </item>
"""

class XmlPrinter(Printer):
    def write(self, items):
        s = ''.join([XML_ITEM_FORMAT.format(*map(html_escape, i)) for i in items])
        print XML_ITEMS_FORMAT.format(s)

JSON_ITEMS_FORMAT = """{{
{0}}}"""
JSON_ITEM_FORMAT = """   {{ "uid": "{0}", "arg": "{2}", "autocomplete": "{1}", "valid": "{5}", "title": "{2}", "subtitle": "{3}", "icon": "{4}" }}
"""

class JsonPrinter(Printer):
    def write(self, items):
        s = ''.join([JSON_ITEM_FORMAT.format(*map(html_escape, i)) for i in items])
        print JSON_ITEMS_FORMAT.format(s)

SIMPLE_ITEMS_FORMAT = """Id\tTitle\tSubtitle\tAutocomplete\t
{0}"""
SIMPLE_ITEM_FORMAT = """{0}\t{2}\t{3}\t{1}
"""

class SimplePrinter(Printer):
    def write(self, items):
        s = ''.join([SIMPLE_ITEM_FORMAT.format(*map(html_escape, i)) for i in items])
        print SIMPLE_ITEMS_FORMAT.format(s)
