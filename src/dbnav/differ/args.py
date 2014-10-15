#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse

from dbnav.args import parent_parser, format_group

from .writer import DiffWriter, DiffTestWriter

parent = parent_parser()

group = format_group(parent, DiffTestWriter)
group.add_argument('-D',
	'--default',
	default=True,
	help='output format: human readable hierarchical text',
	dest='formatter',
	action='store_const',
	const=DiffWriter)

parser = argparse.ArgumentParser(
    prog='dbdiff',
    description='A diff tool that compares the structure of two database tables with each other',
    formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    parents=[parent])
parser.add_argument('left',
	help='the left URI to parse (format for PostgreSQL: user@host/database/table; for SQLite: databasefile.db/table)')
parser.add_argument('right',
	help='the right URI to parse (format for PostgreSQL: user@host/database/table; for SQLite: databasefile.db/table)')
parser.add_argument('--verbose', '-v', action='count', help='specify the verbosity of the output, increase the number of occurences of this option to increase verbosity')
