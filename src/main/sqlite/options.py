#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ..options import *

class SQLiteOptions(Options):
    def parse_options(self):
        Options.parse_options(self)
        if self.uri:
            paths = self.uri.split('/')
            if len(paths) > 1: self.table = paths[1]
            if len(paths) > 2:
                self.column = paths[2]
                for operator in '=~':
                    if operator in self.column:
                        self.operator = operator
                        f = self.column.split(operator, 1)
                        self.column = f[0]
                        if len(f) > 1:
                            self.filter = f[1]
                        break
            self.show = {
                1: 'connections',
                2: 'tables',
                3: 'columns',
                4: 'values'
            }.get(len(paths), 'connections')
