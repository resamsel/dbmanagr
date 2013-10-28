#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import logging
import argparse

from urlparse import urlparse

from .printer import *
from .item import *

OPTION_URI_FORMAT = '%s@%s/%s'

logger = logging.getLogger(__name__)

def parse_loglevel(level):
    numeric_level = getattr(logging, level.upper(), None)
    if not isinstance(numeric_level, int):
        e = ValueError('Invalid log level: %s' % level)
        Printer.write([Item(str(e), type(e), '', 'no', '')])
        sys.exit()
    return numeric_level

class Options:
    arg = None
    user = None
    host = None
    database = None
    table = None
    filter = None
    display = False
    loglevel = logging.WARNING
    logfile = '/tmp/dbnavigator.log'

    @staticmethod
    def init():
        parser = argparse.ArgumentParser()
        parser.add_argument('uri', help='The URI to parse', nargs='?')
        group = parser.add_mutually_exclusive_group()
        group.add_argument('-d', '--default', help='use default printer', action='store_true')
        group.add_argument('-s', '--simple', help='use simple printer', action='store_true')
        group.add_argument('-j', '--json', help='use JSON printer', action='store_true')
        group.add_argument('-x', '--xml', help='use XML printer', action='store_true')
        parser.add_argument('-f', '--logfile', help='the file to log to')
        parser.add_argument('-l', '--loglevel', help='the minimum level to log')
        args = parser.parse_args()

        loglevel_env = os.getenv("LOGLEVEL")
        if loglevel_env:
            Options.loglevel = parse_loglevel(loglevel_env)

        logfile_env = os.getenv("LOGFILE")
        if logfile_env:
            Options.logfile = logfile_env

        if args.default: Printer.set(DefaultPrinter())
        if args.simple: Printer.set(SimplePrinter())
        if args.json: Printer.set(JsonPrinter())
        if args.xml: Printer.set(XmlPrinter())
        if args.uri: Options.arg = args.uri
        if args.logfile: Options.logfile = args.logfile
        if args.loglevel: Options.loglevel = parse_loglevel(args.loglevel)

        if Options.arg:
            arg = Options.arg
            if '@' not in arg:
                arg += '@'
            url = urlparse('postgres://%s' % arg)
            locs = url.netloc.split('@')
            Options.paths = url.path.split('/')

            if len(locs) > 0:  Options.user = locs[0]
            if '@' in Options.arg: Options.host = locs[1]
            if len(Options.paths) > 1: Options.database = Options.paths[1]
            if len(Options.paths) > 2: Options.table = Options.paths[2]
            if len(Options.paths) > 3: Options.filter = Options.paths[3]
            Options.display = arg.endswith('/')

        Options.uri = None
        if Options.user and Options.host:
            Options.uri = OPTION_URI_FORMAT % (Options.user, Options.host, Options.table if Options.table else '')

        logger.debug('Options: %s' % Options.repr())

    @staticmethod
    def repr():
        return Options.__dict__.__repr__()
