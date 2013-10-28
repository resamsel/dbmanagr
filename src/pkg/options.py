#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging

from urlparse import urlparse

from .printer import *

OPTION_URI_FORMAT = '%s@%s/%s'

logger = logging.getLogger(__name__)

class Options:
    arg = None
    user = None
    host = None
    database = None
    table = None
    filter = None
    display = False

    @staticmethod
    def init(args):
        if len(args) > 1 and args[1].startswith('-'):
            Printer.set(args[1])
            del args[1]
            
        if len(args) > 1:
            Options.arg = args[1]
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
