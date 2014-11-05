#!/usr/bin/env python
# -*- coding: utf-8 -*-

from urlparse import urlparse

from dbnav.logger import logger
from dbnav.options import parse_filter

OPTION_URI_FORMAT = '%s@%s/%s'


class PostgreSQLOptions:
    def __init__(self):
        self.user = None
        self.host = None
        self.gen = None

    def get(self, driver):
        return self

    def __repr__(self):
        return str(self.__dict__)


class PostgreSQLOptionsParser:
    def parse(self, source):
        opts = PostgreSQLOptions()
        opts.__dict__.update(source.__dict__)
        if opts.uri:
            uri = opts.uri
            if '@' not in uri:
                uri += '@'
            url = urlparse('postgres://%s' % uri)
            locs = url.netloc.split('@')
            paths = url.path.split('/')

            if len(locs) > 0:
                opts.user = locs[0]
            if '@' in opts.uri:
                opts.host = locs[1]
            if len(paths) > 1:
                opts.database = paths[1]
            if len(paths) > 2:
                opts.table = paths[2]
            if '?' in uri:
                opts.filter = parse_filter(url.query)
                paths.append(url.query)

            opts.show = {
                1: 'connections',
                2: 'databases',
                3: 'tables',
                4: 'columns',
                5: 'values'
            }.get(len(paths), 'connections')

        if opts.user and opts.host:
            opts.gen = OPTION_URI_FORMAT % (
                opts.user, opts.host, opts.table if opts.table else '')

        logger.debug('Parsed options: %s', opts.__dict__)

        return opts
