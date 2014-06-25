#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ..options import *
from urlparse import urlparse

OPTION_URI_FORMAT = '%s@%s/%s'

class PostgreSQLOptions(Options):
    def __init__(self):
        Options.__init__(self)
        self.gen = None
        self.user = None
        self.host = None

    def parse_options(self):
        Options.parse_options(self)
        if self.uri:
            uri = self.uri
            if '@' not in uri:
                uri += '@'
            url = urlparse('postgres://%s' % uri)
            locs = url.netloc.split('@')
            paths = url.path.split('/')

            if len(locs) > 0: self.user = locs[0]
            if '@' in self.uri: self.host = locs[1]
            if len(paths) > 1: self.database = paths[1]
            if len(paths) > 2: self.table = paths[2]
            if len(paths) > 3:
                self.column = paths[3]
                for operator in '=~*':
                    if operator in self.column:
                        self.operator = operator
                        f = self.column.split(operator, 1)
                        self.column = f[0]
                        if len(f) > 1:
                            self.filter = f[1]
                        break
            self.show = {
                1: 'connections',
                2: 'databases',
                3: 'tables',
                4: 'columns',
                5: 'values'
            }.get(len(paths), 'connections')

        if self.user and self.host:
            self.gen = OPTION_URI_FORMAT % (self.user, self.host, self.table if self.table else '')
        
        logger.debug('Parsed options: %s', self.__dict__)
