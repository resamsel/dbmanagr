#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging

class Row:
    """A table row from the database"""

    def __init__(self, connection, table, row):
        self.connection = connection
        self.table = table
        self.row = row

    def __getitem__(self, i):
        if isinstance(i, unicode):
            i = i.encode('ascii')
        logging.debug('row[%s], type: %s' % (str(i), type(i)))
        return self.row[i]

    def values(self):
        return self.row
