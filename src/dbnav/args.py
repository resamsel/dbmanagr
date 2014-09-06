#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import argparse
from dbnav.writer import TestWriter

def default_log_file():
    for d in ['/var/log', '/usr/local/var/log', '/tmp']:
        if os.access(d, os.W_OK):
            return os.path.join(d, 'dbnav.log')
    return os.path.expanduser('~/dbnav.log')

def parent_parser():
    parser = argparse.ArgumentParser(add_help=False)
    group = parser.add_argument_group('logging')
    group.add_argument('-f',
		'--logfile',
        type=argparse.FileType('w'),
		default=default_log_file(),
		help='the file to log to')
    group.add_argument('-l',
		'--loglevel',
		default='warning',
        choices=['critical', 'error', 'warning', 'info', 'debug'],
		help='the minimum level to log')
    return parser

def format_group(parser, test_writer=TestWriter):
    group = parser.add_argument_group('formatters')
    group.add_argument('-t',
		'--test',
		help='output format: test specific',
		dest='formatter',
		action='store_const',
		const=test_writer)
    return group
