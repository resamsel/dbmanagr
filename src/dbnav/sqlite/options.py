#!/usr/bin/env python
# -*- coding: utf-8 -*-

from urlparse import urlparse

from dbnav.options import parse_filter


class SQLiteOptions:
    def get(self, driver):
        return self

    def __repr__(self):
        return str(self.__dict__)


class SQLiteOptionsParser:
    def parse(self, source):
        opts = SQLiteOptions()
        opts.__dict__.update(source.__dict__)
        if opts.uri:
            uri = opts.uri
            url = urlparse('sqlite://%s' % uri)
            paths = url.path.split('/')
 
            if len(paths) > 1:
                opts.table = paths[1]
            if '?' in uri:
                opts.filter = parse_filter(url.query)
                paths.append(url.query)

            opts.show = {
                1: 'connections',
                2: 'tables',
                3: 'columns',
                4: 'values'
            }.get(len(paths), 'connections')

        return opts