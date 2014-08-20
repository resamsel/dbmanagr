#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import logging

from dbnav.writer import *
from dbnav.item import *

logger = logging.getLogger(__name__)

def parse_loglevel(level):
    numeric_level = getattr(logging, level.upper(), None)
    if not isinstance(numeric_level, int):
        e = ValueError('Invalid log level: %s' % level)
        Writer.write([Item(str(e), type(e), '', 'no', '')])
        sys.exit()
    return numeric_level

class Options:
    parser = {}

    def __init__(self, argv, parser):
        logger.info('Called with params: %s', argv)

        self.opts = {}
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
        self.artificial_projection = True
        self.default = False
        self.simple = False
        self.json = False
        self.xml = False
        self.autocomplete = False

        args = parser.parse_args(argv[1:])

        if args.loglevel:
            args.loglevel = parse_loglevel(args.loglevel)
        if hasattr(args, 'include'):
            args.include = args.include.split(',') if args.include else []
        if hasattr(args, 'exclude'):
            args.exclude = args.exclude.split(',') if args.exclude else []

        self.__dict__.update(args.__dict__)
        
        Writer.from_options(self)

        for k in Options.parser:
            self.opts[k] = Options.parser[k].parse(self)

    def get(self, parser):
        return self.opts[parser]

    def __setattr__(self, name, value):
        self.__dict__[name] = value
        if self.opts:
            for k in self.opts.keys():
                self.opts[k].__dict__[name] = value

    def __repr__(self):
        return self.__dict__.__repr__()
