#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import logging
import argparse

from .printer import *
from .item import *

logger = logging.getLogger(__name__)

def parse_loglevel(level):
    numeric_level = getattr(logging, level.upper(), None)
    if not isinstance(numeric_level, int):
        e = ValueError('Invalid log level: %s' % level)
        Printer.write([Item(str(e), type(e), '', 'no', '')])
        sys.exit()
    return numeric_level

class Options:
    uri = None
    parser = {}
    logfile = None
    loglevel = None

    @staticmethod
    def init():
        parser = argparse.ArgumentParser(prog='dbnav')
        parser.add_argument('uri', help="""The URI to parse. Format for PostgreSQL: user@host/database/table/filter/; for SQLite: databasefile.db/table/filter/""", nargs='?')
        group = parser.add_mutually_exclusive_group()
        group.add_argument('-d', '--default', help='use default printer', action='store_true')
        group.add_argument('-s', '--simple', help='use simple printer', action='store_true')
        group.add_argument('-j', '--json', help='use JSON printer', action='store_true')
        group.add_argument('-x', '--xml', help='use XML printer', action='store_true')
        group.add_argument('-a', '--autocomplete', help='use autocomplete printer', action='store_true')
        parser.add_argument('-f', '--logfile', default='/tmp/dbnavigator.log', help='the file to log to')
        parser.add_argument('-l', '--loglevel', default='warning', help='the minimum level to log')
        args = parser.parse_args()

        if args.default: Printer.set(DefaultPrinter())
        if args.simple: Printer.set(SimplePrinter())
        if args.json: Printer.set(JsonPrinter())
        if args.xml: Printer.set(XmlPrinter())
        if args.autocomplete: Printer.set(AutocompletePrinter())
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

    @staticmethod
    def repr():
        return Options.__dict__.__repr__()
