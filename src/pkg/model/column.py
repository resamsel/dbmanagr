#!/usr/bin/env python
# -*- coding: utf-8 -*-

class Column:
    """A table column"""

    def __init__(self, table, name):
        self.table = table
        self.name = name

    def __repr__(self):
        return '%s.%s' % (self.table.name, self.name)
