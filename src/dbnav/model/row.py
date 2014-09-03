#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
from dbnav.model.baseitem import BaseItem
from dbnav.formatter import Formatter

logger = logging.getLogger(__name__)

def val(row, column):
    colname = '%s_title' % column
    if colname in row.row:
        return '%s (%s)' % (row.row[colname], row.row[column])
    return row.row[column]

class Row(BaseItem):
    """A table row from the database"""

    def __init__(self, connection, table, row):
        self.connection = connection
        self.table = table
        self.row = row

    def __getitem__(self, i):
        #logger.debug('Row.__getitem__(%s: %s)', str(i), type(i))
        if i == None:
            return None
        if type(i) == unicode:
            i = i.encode('ascii')
        return self.row[i]

    def values(self):
        return self.row

    def __repr__(self):
        return str(self.row)

    def title(self):
        return val(self, 'title')

    def subtitle(self):
        return val(self, 'subtitle')

    def autocomplete(self):
        return '%s?%s=%s' % (
            self.table.autocomplete(),
            self.table.primary_key,
            self[self.table.primary_key])

    def icon(self):
        return 'images/row.png'

    def format(self):
        return Formatter.format_row(self)
