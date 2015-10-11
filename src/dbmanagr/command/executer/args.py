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

import argparse
import sys

from dbmanagr.args import parent_parser, format_group, create_parser

from .writer import ExecuteWriter, SqlInsertWriter, ExecuteTestWriter

parent = parent_parser()

group = format_group(parent, ExecuteTestWriter)
group.add_argument(
    '-D',
    '--default',
    help='output format: tuples',
    dest='formatter',
    action='store_const',
    const=ExecuteWriter)
group.add_argument(
    '-I',
    '--insert',
    help='output format: SQL insert statements',
    dest='formatter',
    action='store_const',
    const=SqlInsertWriter)

parser = create_parser(
    prog='dbexec',
    description='Executes the SQL statements from the given file on the '
                'database specified by the given URI',
    parents=[parent])
parser.add_argument(
    'uri',
    help='the URI to parse (format for PostgreSQL/MySQL: user@host/database; '
         'for SQLite: databasefile.db)')
parser.add_argument(
    'infile',
    default=[sys.stdin],
    help='the path to the file containing the SQL query to execute (default: '
         'standard input)',
    type=argparse.FileType('r'),
    nargs='*')
parser.add_argument(
    '-s',
    '--statements',
    help='the statements to execute (infile will be ignored when this '
         'parameter is given)')
parser.add_argument(
    '-p',
    '--progress',
    default=-1,
    type=int,
    help='show progress after this amount of executions when inserting/'
         'updating large data sets (default: %(default)s)')
parser.add_argument(
    '-t',
    '--table-name',
    default='__TABLE__',
    help='the table name for generic select statements (default: %(default)s)')
parser.add_argument(
    '-n',
    '--dry-run',
    action='store_true',
    default=False,
    help='Do a rollback after execution')
parser.add_argument(
    '--isolate-statements',
    action='store_true',
    default=False,
    help='Wrap each statement in a separate transaction - this allows '
         'continuing execution even if an SQL statement fails')
parser.add_argument(
    '--mute-errors',
    action='store_true',
    default=False,
    help='Don\'t display error message for failing statements')
parser.add_argument(
    '-v',
    '--verbose',
    action='count',
    help='specify the verbosity of the output, increase the number of '
         'occurences of this option to increase verbosity')
