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

from dbmanagr.args import parent_parser, format_group, create_parser

from .writer import ArgumentWriter, ArgumentTestWriter, ArgumentVerboseWriter

parent = parent_parser(daemonable=True)

group = format_group(
    parent,
    ArgumentTestWriter)
group.add_argument(
    '-D',
    '--default',
    default=True,
    help='output format: human readable hierarchical text',
    dest='formatter',
    action='store_const',
    const=ArgumentWriter)
group.add_argument(
    '-V',
    help='output format: better readable text',
    dest='formatter',
    action='store_const',
    const=ArgumentVerboseWriter)

parser = create_parser(
    prog='dbargs',
    description='A tool to convert YAML config files to db{graph,export,nav} '
                'command line arguments',
    parents=[parent])
parser.add_argument(
    'infile',
    default='-',
    help='the path to the file containing the YAML config to convert',
    type=argparse.FileType('r'),
    nargs='?')
parser.add_argument(
    '-i',
    '--includes',
    default=True,
    dest='includes',
    action='store_true',
    help='show includes in output')
parser.add_argument(
    '-I',
    '--no-includes',
    dest='includes',
    action='store_false',
    help='hide includes in output')
parser.add_argument(
    '-x',
    '--excludes',
    default=True,
    dest='excludes',
    action='store_true',
    help='show excludes in output')
parser.add_argument(
    '-X',
    '--no-excludes',
    dest='excludes',
    action='store_false',
    help='hide excludes in output')
parser.add_argument(
    '-s',
    '--substitutes',
    default=True,
    dest='substitutes',
    action='store_true',
    help='show substitutes in output')
parser.add_argument(
    '-S',
    '--no-substitutes',
    dest='substitutes',
    action='store_false',
    help='hide substitutes in output')

parser.add_argument(
    '-v',
    '--verbose',
    action='count',
    help='specify the verbosity of the output, increase the number of '
         'occurences of this option to increase verbosity')
