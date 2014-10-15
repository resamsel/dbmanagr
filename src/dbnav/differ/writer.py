#!/usr/bin/env python
# -*- coding: utf-8 -*-

from dbnav.writer import FormatWriter
from dbnav.formatter import Formatter, DefaultFormatter

def value_from_column(column, config):
    if config.verbose > 2:
        return column.autocomplete()
    if config.verbose > 1:
        return '/'.join(column.autocomplete().split('/')[1:])
    elif config.verbose > 0:
        return unicode(column)
    return column.name

class DiffWriter(FormatWriter):
    def __init__(self, left=None, right=None):
        FormatWriter.__init__(self, u'{0}')
        Formatter.set(DefaultFormatter())
        self.left = left
        self.right = right
    def str(self, items):
        if not items:
            return 'No differences found'
        s = self.item_separator.join(
            map(lambda i: self.itemtostring(i),
                self.filter(items)))
        return self.items_format.format(s)
    def itemtostring(self, item):
        if item.left:
            return u'< {0}'.format(value_from_column(item.column, self.left))
        else:
            return u'> {0}'.format(value_from_column(item.column, self.right))

class DiffTestWriter(DiffWriter):
    pass
