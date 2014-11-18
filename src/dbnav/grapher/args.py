#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse

from dbnav.args import parent_parser, format_group

from .writer import GraphWriter, GraphvizWriter, GraphTestWriter

parent = parent_parser()

group = format_group(
    parent,
    GraphTestWriter)
group.add_argument(
    '-D',
    '--default',
    default=True,
    help='output format: human readable hierarchical text',
    dest='formatter',
    action='store_const',
    const=GraphWriter)
group.add_argument(
    '-G',
    '--graphviz',
    help='output format: a Graphviz graph',
    dest='formatter',
    action='store_const',
    const=GraphvizWriter)

parser = argparse.ArgumentParser(
    prog='dbgraph',
    description='A database visualisation tool that creates graphs from the '
                'database structure',
    parents=[parent])
parser.add_argument(
    'uri',
    help='the URI to parse (format for PostgreSQL/MySQL: '
         'user@host/database/table; for SQLite: databasefile.db/table)')
parser.add_argument(
    '-c',
    '--columns',
    dest='include_columns',
    default=False,
    help='include columns in output',
    action='store_true')
parser.add_argument(
    '-C',
    '--no-columns',
    dest='include_columns',
    default=True,
    help='don\'t include columns in output',
    action='store_false')
parser.add_argument(
    '--back-references',
    dest='include_back_references',
    default=True,
    help='include back references in output',
    action='store_true')
parser.add_argument(
    '--no-back-references',
    dest='include_back_references',
    default=False,
    help='don\'t include back references in output',
    action='store_false')
parser.add_argument(
    '--driver',
    dest='include_driver',
    default=False,
    help='include database driver in output (does not work well with graphviz '
         'as output)',
    action='store_true')
parser.add_argument(
    '--no-driver',
    dest='include_driver',
    default=True,
    help='don\'t include database driver in output',
    action='store_false')
parser.add_argument(
    '--connection',
    dest='include_connection',
    default=False,
    help='include connection in output (does not work well with graphviz as '
         'output)',
    action='store_true')
parser.add_argument(
    '--no-connection',
    dest='include_connection',
    default=True,
    help='don\'t include connection in output',
    action='store_false')
parser.add_argument(
    '--database',
    dest='include_database',
    default=False,
    help='include database in output (does not work well with graphviz as '
         'output)',
    action='store_true')
parser.add_argument(
    '--no-database',
    dest='include_database',
    default=True,
    help='don\'t include database in output',
    action='store_true')
parser.add_argument(
    '-M',
    '--max-depth',
    default=-1,
    type=int,
    help='the maximum depth to use in recursion/inclusion (default: '
         '%(default)s)')

group = parser.add_mutually_exclusive_group()
group.add_argument(
    '-r',
    '--recursive',
    help='include any forward/back reference to the starting table, recursing '
         'through all tables eventually',
    action='store_true')
group.add_argument(
    '-i',
    '--include',
    help='include the specified columns and their foreign rows, if any. '
         'Multiple columns can be specified by separating them with a comma '
         '(,)')
parser.add_argument(
    '-x',
    '--exclude',
    help='exclude the specified columns')
parser.add_argument(
    '-v',
    '--verbose',
    action='count',
    help='specify the verbosity of the output, increase the number of '
         'occurences of this option to increase verbosity')
