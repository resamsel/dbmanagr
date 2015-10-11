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
from dbmanagr.args import CommaSeparatedDict

from .writer import SqlInsertWriter, SqlUpdateWriter, SqlDeleteWriter
from .writer import YamlWriter, FormattedWriter

parent = parent_parser(daemonable=True)

group = format_group(
    parent,
    SqlInsertWriter)
group.add_argument(
    '-I',
    '--insert',
    default=True,
    help='output format: SQL insert statements',
    dest='formatter',
    action='store_const',
    const=SqlInsertWriter)
group.add_argument(
    '-U',
    '--update',
    help='output format: SQL update statements',
    dest='formatter',
    action='store_const',
    const=SqlUpdateWriter)
group.add_argument(
    '-D',
    '--delete',
    help='output format: SQL delete statements',
    dest='formatter',
    action='store_const',
    const=SqlDeleteWriter)
group.add_argument(
    '-Y',
    '--yaml',
    help='output format: YAML data',
    dest='formatter',
    action='store_const',
    const=YamlWriter)
group.add_argument(
    '-F',
    '--formatted',
    help='output format: given with the -f/--format option',
    dest='formatter',
    action='store_const',
    const=FormattedWriter)

parser = create_parser(
    prog='dbexport',
    description='An export tool that exports database rows in different '
                'formats.',
    parents=[parent])
parser.add_argument(
    'uri',
    help='the URI to parse (format for PostgreSQL/MySQL: '
         'user@host/database/table?column=value; for SQLite: '
         'databasefile.db/table?column=value)')
parser.add_argument(
    '-i',
    '--include',
    help='include specified columns; referenced rows, if any, can be included '
         'by adding a dot after the column name; multiple columns can be '
         'specified by separating them with a comma')
parser.add_argument(
    '-x',
    '--exclude',
    help='exclude specified columns')
parser.add_argument(
    '-s',
    '--substitutes',
    action=CommaSeparatedDict,
    help='substitute values of rows with static values, in the form of: '
         'fk.column=replacement; multiple substitutions can be specified by '
         'separating them with a comma')
parser.add_argument(
    '-m',
    '--limit',
    type=int,
    default=50,
    help='limit the results of the main query to this amount of rows '
         '(default: %(default)s)')
parser.add_argument(
    '-p',
    '--package',
    default='models',
    help='the package for YAML entities (default: %(default)s)')
parser.add_argument(
    '-f',
    '--format',
    default=u'{0}',
    help='the format for the -F/--formatted writer (use {0} for positional '
         'arguments, or {column_name} to insert the actual value of '
         'table.column_name) (default: %(default)s)')
