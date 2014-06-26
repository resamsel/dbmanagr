#!/usr/bin/env python
# -*- coding: utf-8 -*-

from dbnav.options import *

class SQLiteOptions:
    def get(self, driver):
        return self

class SQLiteOptionsParser:
    def parse(self, source):
        opts = SQLiteOptions()
        opts.__dict__.update(source.__dict__)
        if opts.uri:
            paths = opts.uri.split('/')
            if len(paths) > 1: opts.table = paths[1]
            if len(paths) > 2:
                opts.column = paths[2]
                for operator in '=~*':
                    if operator in opts.column:
                        opts.operator = operator
                        f = opts.column.split(operator, 1)
                        opts.column = f[0]
                        if len(f) > 1:
                            opts.filter = f[1]
                        break
            opts.show = {
                1: 'connections',
                2: 'tables',
                3: 'columns',
                4: 'values'
            }.get(len(paths), 'connections')

        return opts