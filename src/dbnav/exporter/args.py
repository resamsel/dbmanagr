#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse

from dbnav.args import parent_parser, format_group

from .writer import SqlInsertWriter, SqlUpdateWriter, SqlDeleteWriter
from .writer import YamlWriter, FormattedWriter

parent = parent_parser()

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

parser = argparse.ArgumentParser(
    prog='dbexport',
    description='An export tool that exports database rows in different '
                'formats.',
    formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    parents=[parent])
parser.add_argument(
    'uri',
    help='the URI to parse (format for PostgreSQL/MySQL: '
         'user@host/database/table?column=value; for SQLite: '
         'databasefile.db/table?column=value)')
parser.add_argument(
    '-i',
    '--include',
    help='include the specified columns and their foreign rows, if any '
         '(multiple columns can be specified by separating them with a comma)')
parser.add_argument(
    '-x',
    '--exclude',
    help='Exclude the specified columns')
parser.add_argument(
    '-m',
    '--limit',
    type=int,
    default=50,
    help='limit the results of the main query to this amount of rows')
parser.add_argument(
    '-p',
    '--package',
    default='models',
    help='the package for YAML entities')
parser.add_argument(
    '-f',
    '--format',
    default=u'{0}',
    help='the format for the -F/--formatted writer (use {0} for positional '
         'arguments, or {column_name} to insert the actual value of '
         'table.column_name)')
