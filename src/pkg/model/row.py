#!/usr/bin/env python
# -*- coding: utf-8 -*-

class Row:
    """A table row from the database"""

    def __init__(self, connection, table, row):
        self.connection = connection
        self.table = table
        self.row = row

    def __getitem__(self, i):
        return self.row[i]

    def values(self):
        return self.row
