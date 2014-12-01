#!/usr/bin/env python
# -*- coding: utf-8 -*-

from dbnav.model.baseitem import BaseItem
from dbnav.formatter import Formatter
from dbnav.utils import dictminus


class Column(BaseItem):
    """A table column"""

    def __init__(self, table, name, **kwargs):
        self.table = table
        self.name = name
        self.__dict__.update(kwargs)

    def __repr__(self):
        if self.table:
            return '%s.%s' % (self.table.name, self.name)
        return self.name

    def __str__(self):
        return self.__repr__()

    def ddl(self):
        return '{0} {1}{2}{3}'.format(
            self.name,
            self.type.compile(),
            {False: ' not null'}.get(self.nullable, ''),
            {None: ''}.get(self.default, ' default {0}'.format(self.default)),
            {None: ''}.get(self.autocomplete, ' autoincrement {0}'.format(
                self.autoincrement)))

    def title(self):
        return self.name

    def subtitle(self):
        return self.table.title()

    def autocomplete(self):
        return '%s%s?%s' % (self.table.uri, self.table.name, self.name)

    def icon(self):
        return 'images/table.png'

    def format(self):
        return Formatter.format_column(self)


def create_column(table, name, column):
    return Column(table, name, **dictminus(column.__dict__, 'name', 'table'))
