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
from dbmanagr.writer import TestWriter

from .writer import SimplifiedWriter, SimpleWriter, JsonWriter
from .writer import AutocompleteWriter

parent = parent_parser(daemonable=True)

group = format_group(parent, TestWriter)
group.add_argument(
    '-D',
    '--default',
    help='output format: default',
    dest='formatter',
    action='store_const',
    const=SimplifiedWriter)
group.add_argument(
    '-S',
    '--simple',
    help='output format: simple',
    dest='formatter',
    action='store_const',
    const=SimpleWriter)
group.add_argument(
    '-J',
    '--json',
    help='output format: JSON',
    dest='formatter',
    action='store_const',
    const=JsonWriter)
group.add_argument(
    '-A',
    '--autocomplete',
    help='output format: autocomplete',
    dest='formatter',
    action='store_const',
    const=AutocompleteWriter)
parser = create_parser(
    prog='dbmanagr',
    description='A database navigation tool that shows database structure and'
                ' content',
    parents=[parent])
parser.add_argument(
    'uri',
    help='the URI to parse (format for PostgreSQL/MySQL: '
         'user@host/database/table?filter; for SQLite: '
         'databasefile.db/table?filter)',
    nargs='?')
parser.add_argument(
    '-s',
    '--simplify',
    dest='simplify',
    default=True,
    help='simplify the output',
    action='store_true')
parser.add_argument(
    '-N',
    '--no-simplify',
    dest='simplify',
    help='don\'t simplify the output',
    action='store_false')
parser.add_argument(
    '-m',
    '--limit',
    type=int,
    default=50,
    help='limit the results of the main query to this amount of rows '
         '(default: %(default)s)')
