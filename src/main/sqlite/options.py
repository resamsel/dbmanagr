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
                f = paths[2].split('=')
                self.column = f[0]
                if len(f) > 1:
                    self.filter = f[1]
            self.showtables = len(paths) > 1
            self.showcolumns = len(paths) > 2
            self.showvalues = len(paths) > 3
