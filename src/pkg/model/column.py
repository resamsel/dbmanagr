#!/usr/bin/env python
# -*- coding: utf-8 -*-

class Column:
    """A table column"""

    def __init__(self, table, name, primary_key=False):
        self.table = table
        self.name = name
        self.primary_key = primary_key

    def __repr__(self):
        return '%s.%s' % (self.table.name, self.name)
