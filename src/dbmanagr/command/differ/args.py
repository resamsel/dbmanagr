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

from dbmanagr.args import parent_parser, format_group, create_parser

from .writer import DiffWriter, DiffColumnWriter, DiffTestWriter

parent = parent_parser(daemonable=True)

group = format_group(parent, DiffTestWriter)
group.add_argument(
    '-D',
    '--default',
    default=True,
    help='output format: human readable hierarchical text',
    dest='formatter',
    action='store_const',
    const=DiffWriter)
group.add_argument(
    '-S',
    '--side-by-side',
    help='output format: compare side-by-side in two columns',
    dest='formatter',
    action='store_const',
    const=DiffColumnWriter)

parser = create_parser(
    prog='dbdiff',
    description='A diff tool that compares the structure of two database '
                'tables with each other.',
    parents=[parent])
parser.add_argument(
    'left',
    help='the left URI to parse (format for PostgreSQL/MySQL: '
         'user@host/database/table; for SQLite: databasefile.db/table)')
parser.add_argument(
    'right',
    help='the right URI to parse (format for PostgreSQL/MySQL: '
         'user@host/database/table; for SQLite: databasefile.db/table)')
parser.add_argument(
    '-v',
    '--verbose',
    action='count',
    help='specify the verbosity of the output, increase the number of '
         'occurences of this option to increase verbosity')
parser.add_argument(
    '-c',
    '--compare-ddl',
    default=False,
    action='store_true',
    help='compares the DDLs for each column')
# parser.add_argument('-I', '--ignore-case', help='ignore case differences in '
#                     'table columns')
# parser.add_argument('-q', '--brief', help='output only whether files differ')
# parser.add_argument('-y', '--side-by-side', help='output in two columns')
# parser.add_argument('-r', '--recursive', help='recursively compare any '
#                     'subdirectories found')
# parser.add_argument('-i', '--include', help='include the specified columns '
#                     'and their foreign rows, if any (multiple columns can '
#                     'be specified by separating them with a comma)')
# parser.add_argument('-x', '--exclude', help='Exclude the specified columns')
# parser.add_argument('-s', '--report-identical-tables', help='report when '
#                     'two tables are the same')
