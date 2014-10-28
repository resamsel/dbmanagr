#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse

from dbnav.args import parent_parser, format_group

from .writer import DiffWriter, DiffColumnWriter, DiffTestWriter

parent = parent_parser()

group = format_group(parent, DiffTestWriter)
group.add_argument('-D',
	'--default',
	default=True,
	help='output format: human readable hierarchical text',
	dest='formatter',
	action='store_const',
	const=DiffWriter)
group.add_argument('-S',
	'--side-by-side',
	help='output format: compare side-by-side in two columns',
	dest='formatter',
	action='store_const',
	const=DiffColumnWriter)

parser = argparse.ArgumentParser(
    prog='dbdiff',
    description='A diff tool that compares the structure of two database tables with each other.',
    formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    parents=[parent])
parser.add_argument('left',
	help='the left URI to parse (format for PostgreSQL: user@host/database/table; for SQLite: databasefile.db/table)')
parser.add_argument('right',
	help='the right URI to parse (format for PostgreSQL: user@host/database/table; for SQLite: databasefile.db/table)')
parser.add_argument('-v', '--verbose', action='count', help='specify the verbosity of the output, increase the number of occurences of this option to increase verbosity')
parser.add_argument('-c', '--compare-ddl', default=False, action='store_true', help='compares the DDLs for each column')
#parser.add_argument('-I', '--ignore-case', help='ignore case differences in table columns')
#parser.add_argument('-q', '--brief', help='output only whether files differ')
#parser.add_argument('-y', '--side-by-side', help='output in two columns')
#parser.add_argument('-r', '--recursive', help='recursively compare any subdirectories found')
#parser.add_argument('-i', '--include', help='include the specified columns and their foreign rows, if any (multiple columns can be specified by separating them with a comma)')
#parser.add_argument('-x', '--exclude', help='Exclude the specified columns')
#parser.add_argument('-s', '--report-identical-tables', help='report when two tables are the same')
