#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import logging
import argparse

from dbnav.writer import *
from dbnav.item import *

logger = logging.getLogger(__name__)

parser = argparse.ArgumentParser(prog='dbnav')
parser.add_argument('uri', help="""The URI to parse. Format for PostgreSQL: user@host/database/table/filter/; for SQLite: databasefile.db/table/filter/""", nargs='?')
group = parser.add_mutually_exclusive_group()
group.add_argument('-d', '--default', help='use default writer', action='store_true')
group.add_argument('-s', '--simple', help='use simple writer', action='store_true')
group.add_argument('-j', '--json', help='use JSON writer', action='store_true')
group.add_argument('-x', '--xml', help='use XML writer', action='store_true')
group.add_argument('-a', '--autocomplete', help='use autocomplete writer', action='store_true')
parser.add_argument('-f', '--logfile', default='/tmp/dbnavigator.log', help='the file to log to')
parser.add_argument('-l', '--loglevel', default='warning', help='the minimum level to log')

def parse_loglevel(level):
    numeric_level = getattr(logging, level.upper(), None)
    if not isinstance(numeric_level, int):
        e = ValueError('Invalid log level: %s' % level)
        Writer.write([Item(str(e), type(e), '', 'no', '')])
        sys.exit()
    return numeric_level

class Options:
    parser = {}

    def __init__(self, argv):
        logger.info('Called with params: %s', argv)

        self.argv = argv
        self.uri = None
        self.logfile = None
        self.loglevel = None
        self.database = None
        self.table = None
        self.column = ''
        self.operator = None
        self.filter = None
        self.show = 'connections'
        self.opts = {}

        args = parser.parse_args(argv[1:])

        if args.default: Writer.set(DefaultWriter())
        if args.simple: Writer.set(SimpleWriter())
        if args.json: Writer.set(JsonWriter())
        if args.xml: Writer.set(XmlWriter())
        if args.autocomplete: Writer.set(AutocompleteWriter())
        if args.uri: self.uri = args.uri
        if args.logfile: self.logfile = args.logfile
        if args.loglevel: self.loglevel = parse_loglevel(args.loglevel)

        for k in Options.parser:
            self.opts[k] = Options.parser[k].parse(self)

    def get(self, parser):
        return self.opts[parser]

    def __repr__(self):
        return self.__dict__.__repr__()
