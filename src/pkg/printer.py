#!/usr/bin/env python
# -*- coding: utf-8 -*-

def html_escape(s):
    if isinstance(s, unicode):
        s = s.encode('ascii', 'ignore')
    if type(s) == str:
        return s.replace('&', '&amp;').replace('"', '&quot;').replace('<', '&lt;')
    return s

class DefaultPrinter:
    def write(self, items):
        print map(lambda item: self.itemtostring(item), items)
    def itemtostring(self, item):
        return str(item)

class XmlPrinter(DefaultPrinter):
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


class JsonPrinter(DefaultPrinter):
    ITEMS_FORMAT = """{{
{0}}}"""
    ITEM_FORMAT = """   {{ "uid": "{uid}", "arg": "{title}", "autocomplete": "{autocomplete}", "valid": "{valid}", "title": "{title}", "subtitle": "{subtitle}", "icon": "{icon}" }}
"""
    def write(self, items):
        s = ''.join([self.itemtostring(i) for i in items])
        print JsonPrinter.ITEMS_FORMAT.format(s)
    def itemtostring(self, item):
        return JsonPrinter.ITEM_FORMAT.format(**item.escaped(html_escape))

class SimplePrinter(DefaultPrinter):
    ITEMS_FORMAT = """Id\tTitle\tSubtitle\tAutocomplete
{0}"""
    ITEM_FORMAT = """{uid}\t{title}\t{subtitle}\t{autocomplete}
"""
    def write(self, items):
        s = ''.join([self.itemtostring(i) for i in items])
        print SimplePrinter.ITEMS_FORMAT.format(s)
    def itemtostring(self, item):
        return SimplePrinter.ITEM_FORMAT.format(**item.escaped(html_escape))

class Printer:
    printer = DefaultPrinter()

    @staticmethod
    def set(arg):
        Printer.printer = {
            '-x': XmlPrinter(),
            '-s': SimplePrinter(),
            '-j': JsonPrinter(),
            '-p': DefaultPrinter()
        }.get(arg, DefaultPrinter())

    @staticmethod
    def write(items):
        Printer.printer.write(items)
