#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import argparse
import logging

from dbnav.writer import TestWriter
from dbnav.version import __version__
from dbnav import __drivers__


class LogLevel(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        if values == 'trace':
            values = 'debug'
            setattr(namespace, 'trace', True)
        setattr(
            namespace,
            self.dest,
            getattr(logging, str(values.upper()), None))


def default_log_file():
    for d in ['/var/log', '/usr/local/var/log', '/tmp']:
        if os.access(d, os.W_OK):
            return os.path.join(d, 'dbnav.log')
    return os.path.expanduser('~/dbnav.log')


def parent_parser():
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument(
        '--version',
        action='version',
        version='%(prog)s {version} (drivers: {drivers})'.format(
            version=__version__, drivers=', '.join(__drivers__)))
    group = parser.add_argument_group('logging')
    group.add_argument(
        '-L',
        '--logfile',
        type=argparse.FileType('a'),
        default=default_log_file(),
        help='the file to log to')
    group.add_argument(
        '-l',
        '--loglevel',
        action=LogLevel,
        default=logging.WARNING,
        choices=['critical', 'error', 'warning', 'info', 'debug', 'trace'],
        help='the minimum level to log')
    group.add_argument(
        '--trace',
        action='store_true',
        default=False,
        help='trace any exception that occurs')
    return parser


def format_group(parser, test_writer=TestWriter):
    group = parser.add_argument_group('formatters')
    group.add_argument(
        '-T',
        '--test',
        help='output format: test specific',
        dest='formatter',
        action='store_const',
        const=test_writer)
    return group
