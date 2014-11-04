#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse

from dbnav.args import parent_parser, format_group

from .writer import ExecuteWriter, SqlInsertWriter, ExecuteTestWriter

parent = parent_parser()

group = format_group(parent, ExecuteTestWriter)
group.add_argument('-D',
    '--default',
    help='output format: tuples',
    dest='formatter',
    action='store_const',
    const=ExecuteWriter)
group.add_argument('-I',
    '--insert',
    help='output format: SQL insert statements',
    dest='formatter',
    action='store_const',
    const=SqlInsertWriter)

parser = argparse.ArgumentParser(prog='dbexec',
    description='Executes the SQL statements from the given file on the database specified by the given URI',
    formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    parents=[parent])
parser.add_argument('uri',
    help="""the URI to parse (format for PostgreSQL/MySQL: user@host/database; for SQLite: databasefile.db)""")
parser.add_argument('infile',
    default='-',
    help='the path to the file containing the SQL query to execute',
    type=argparse.FileType('r'),
    nargs='?')
parser.add_argument('-s',
    '--statements',
    help='the statements to execute (infile will be ignored when this parameter is given)')

parser.add_argument('-p',
    '--progress',
    default=-1,
    type=int,
    help='show progress after this amount of executions when inserting/updating large data sets')
parser.add_argument('-n', '--table-name', default='__TABLE__', help='the table name for generic select statements')
