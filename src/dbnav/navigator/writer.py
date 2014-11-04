#!/usr/bin/env python
# -*- coding: utf-8 -*-

from dbnav.writer import FormatWriter
from dbnav.formatter import Formatter, SimplifiedFormatter, XmlFormatter, JsonFormatter, SimpleFormatter, AutocompleteFormatter
from dbnav.item import Item


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


class JsonWriter(FormatWriter):
    def __init__(self):
        FormatWriter.__init__(self,
            u"""[
{0}
]""", item_separator=u""",
""",)
        Formatter.set(JsonFormatter())


class AutocompleteWriter(FormatWriter):
    def __init__(self):
        FormatWriter.__init__(self, u'{0}', u'{autocomplete}')
        Formatter.set(AutocompleteFormatter())


class SimpleWriter(FormatWriter):
    def __init__(self):
        FormatWriter.__init__(self,
            u"""Id\tTitle\tSubtitle\tAutocomplete
{0}""")
        Formatter.set(SimpleFormatter())
