#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging

logger = logging.getLogger(__name__)

class Row:
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

    def autocomplete(self, pk, value):
        return '%s%s=%s/' % (self.table.autocomplete(), pk, value)
