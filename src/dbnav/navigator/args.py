#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse

from dbnav.args import parent_parser, format_group

from .writer import SimplifiedWriter, SimpleWriter, JsonWriter, XmlWriter
from .writer import AutocompleteWriter

parent = parent_parser()

group = format_group(parent)
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
    '-X',
    '--xml',
    help='output format: XML',
    dest='formatter',
    action='store_const',
    const=XmlWriter)
group.add_argument(
    '-A',
    '--autocomplete',
    help='output format: autocomplete',
    dest='formatter',
    action='store_const',
    const=AutocompleteWriter)
parser = argparse.ArgumentParser(
    prog='dbnav',
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
