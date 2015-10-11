# -*- coding: utf-8 -*-
#
# Copyright © 2014 René Samselnig
#
# This file is part of Database Navigator.
#
# Database Navigator is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Database Navigator is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Database Navigator.  If not, see <http://www.gnu.org/licenses/>.
#

import os
import argparse
import logging

from dbmanagr.version import __version__
from dbmanagr import __drivers__

PARSER_ARGS = {
    'formatter_class': argparse.RawDescriptionHelpFormatter,
    'epilog': """Contact:
  If you experience bugs or want to request new features please visit
  <https://github.com/resamsel/dbmanagr/issues>"""
}


class CommaSeparatedDict(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        setattr(
            namespace,
            self.dest,
            dict(map(
                lambda s: map(
                    lambda s: s.strip(),
                    (s.split('=', 1) + [''])[:2]),
                filter(len, values.split(','))))
        )


class CommaSeparatedStringList(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        setattr(
            namespace,
            self.dest,
            ','.join(map("'{0}'".format, values.split(',')))
        )


class CommaSeparatedPlainList(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        setattr(
            namespace,
            self.dest,
            ','.join(values.split(','))
        )


def default_log_file(dirs=None):
    if dirs is None:
        dirs = ['/var/log', '/usr/local/var/log', '/tmp']
    for d in dirs:
        if os.access(d, os.W_OK):
            return os.path.join(d, 'dbmanagr.log')
    return os.path.expanduser('~/dbmanagr.log')


def parent_parser(daemonable=False, daemon=False):
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument(
        '--version',
        action='version',
        version='%(prog)s {version} (drivers: {drivers})'.format(
            version=__version__, drivers=', '.join(__drivers__)))
    group = parser.add_argument_group('logging')
    group.add_argument(
        '--trace',
        action='store_true',
        default=False,
        help='set loglevel to trace')
    group.add_argument(
        '--debug',
        dest='loglevel',
        action='store_const',
        const=logging.DEBUG,
        help='set loglevel to debug')
    group.add_argument(
        '--info',
        dest='loglevel',
        action='store_const',
        const=logging.INFO,
        help='set loglevel to info')
    group.add_argument(
        '--warning',
        dest='loglevel',
        action='store_const',
        const=logging.WARNING,
        help='set loglevel to warning')
    group.add_argument(
        '--error',
        dest='loglevel',
        action='store_const',
        const=logging.ERROR,
        help='set loglevel to error')
    group.add_argument(
        '--critical',
        dest='loglevel',
        action='store_const',
        const=logging.CRITICAL,
        help='set loglevel to critical')
    group.add_argument(
        '-L',
        '--logfile',
        type=argparse.FileType('a'),
        default=default_log_file(),
        help='the file to log to')
    if daemonable:
        group = parser.add_argument_group('daemon')
        if daemon:
            group.add_argument(
                '--host',
                default='',
                help='the host of the daemon')
            group.add_argument(
                '--port',
                default=8020,
                type=int,
                help='the port of the daemon')
        else:
            group.add_argument(
                '--daemon',
                action='store_true',
                default=False,
                help='use a background process to speed up requests')
            group.add_argument(
                '--daemon-host',
                dest='host',
                default='',
                help='the host of the daemon')
            group.add_argument(
                '--daemon-port',
                dest='port',
                default=8020,
                type=int,
                help='the port of the daemon')
    return parser


def format_group(parser, test_writer=None):
    group = parser.add_argument_group('formatters')
    if test_writer:
        group.add_argument(
            '-T',
            '--test',
            help='output format: test specific',
            dest='formatter',
            action='store_const',
            const=test_writer)
    return group


def create_parser(**kwargs):
    kwargs.update(PARSER_ARGS)
    return argparse.ArgumentParser(**kwargs)
