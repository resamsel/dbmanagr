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
from dbmanagr.args import CommaSeparatedPlainList, CommaSeparatedStringList

from .writer import StatementActivityWriter

parent = parent_parser()

group = format_group(parent)
group.add_argument(
    '-D',
    '--default',
    help='output format: default',
    dest='formatter',
    action='store_const',
    const=StatementActivityWriter)

parser = create_parser(
    prog='dbstac',
    description='Lists the statements and transactions currently active in '
                'the DBMS.',
    parents=[parent])
parser.add_argument(
    'uri',
    help='the URI to a DBMS')
parser.add_argument(
    'pattern',
    default=None,
    help='shows only queries that match the pattern (default: no pattern)',
    nargs='?')
parser.add_argument(
    '-u',
    '--username',
    default='',
    help='filter the user')
parser.add_argument(
    '-p',
    '--pids',
    action=CommaSeparatedPlainList,
    default=-1,
    help='filter the process ids of the activity; multiple columns can be '
         'specified by separating them with a comma')
parser.add_argument(
    '-s',
    '--states',
    action=CommaSeparatedStringList,
    default="''",
    help='filter the states of the activity; multiple columns can be '
         'specified by separating them with a comma')
parser.add_argument(
    '-a',
    '--all',
    dest='disabled',
    default=False,
    action='store_true',
    help='show all activity, even those with insufficient privileges')
parser.add_argument(
    '-v',
    '--verbose',
    action='count',
    help='specify the verbosity of the output, increase the number of '
         'occurences of this option to increase verbosity')
