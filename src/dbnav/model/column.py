#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
from dbnav.model.baseitem import BaseItem
from dbnav.formatter import Formatter

logger = logging.getLogger(__name__)


class Column(BaseItem):
    """A table column"""

    def __init__(self, table, name, primary_key=False, type=None, nullable=None, default=None, autoincrement=None):
        self.table = table
        self.name = name
        self.primary_key = primary_key
        self.type = type
        self.nullable = nullable
        self.default = default
        self.autoincrement = autoincrement

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
            {None: ''}.get(self.autocomplete, ' autoincrement {0}'.format(self.autoincrement)))

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
