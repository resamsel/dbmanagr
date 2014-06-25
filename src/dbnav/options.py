#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import logging
import argparse

from .writer import *
from .item import *

logger = logging.getLogger(__name__)

def parse_loglevel(level):
    numeric_level = getattr(logging, level.upper(), None)
    if not isinstance(numeric_level, int):
        e = ValueError('Invalid log level: %s' % level)
        Writer.write([Item(str(e), type(e), '', 'no', '')])
        sys.exit()
    return numeric_level

class Options:
    argv = None
    uri = None
    parser = {}
    logfile = None
    loglevel = None

    @staticmethod
    def init(argv):
        logger.info('Called with params: %s', argv)

        Options.argv = argv
        Options.uri = None
 
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
        args = parser.parse_args(argv[1:])

        if args.default: Writer.set(DefaultWriter())
        if args.simple: Writer.set(SimpleWriter())
        if args.json: Writer.set(JsonWriter())
        if args.xml: Writer.set(XmlWriter())
        if args.autocomplete: Writer.set(AutocompleteWriter())
        if args.uri: Options.uri = args.uri
        if args.logfile: Options.logfile = args.logfile
        if args.loglevel: Options.loglevel = parse_loglevel(args.loglevel)

        for k in Options.parser:
            Options.parser[k].parse_options()

    def __init__(self):
        self.uri = None
        self.database = None
        self.table = None
        self.column = ''
        self.operator = None
        self.filter = None
        self.show = 'connections'

    def parse_options(self):
        self.uri = Options.uri
        self.database = None
        self.table = None
        self.column = ''
        self.operator = None
        self.filter = None
        self.show = 'connections'

    @staticmethod
    def repr():
        return Options.__dict__.__repr__()
