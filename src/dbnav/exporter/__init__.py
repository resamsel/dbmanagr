#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import time
import sys
import argparse
import re

from collections import OrderedDict

from dbnav.config import Config
from dbnav.item import Item, INVALID
from dbnav.sources import Source
from dbnav.logger import logger, logduration
from dbnav.utils import remove_prefix
from dbnav.querybuilder import QueryFilter
from dbnav.model.databaseconnection import values
from dbnav.formatter import Formatter
from dbnav.writer import Writer, TestWriter
from dbnav.args import parent_parser, format_group
from dbnav.model.exception import UnknownColumnException

from .writer import SqlInsertWriter, SqlUpdateWriter, SqlDeleteWriter, YamlWriter

parent = parent_parser()

group = format_group(parent, SqlInsertWriter)
group.add_argument('-I', '--insert', default=True, help='output format: SQL insert statements', dest='formatter', action='store_const', const=SqlInsertWriter)
group.add_argument('-U', '--update', help='output format: SQL update statements', dest='formatter', action='store_const', const=SqlUpdateWriter)
group.add_argument('-D', '--delete', help='output format: SQL delete statements', dest='formatter', action='store_const', const=SqlDeleteWriter)
group.add_argument('-Y', '--yaml', help='output format: YAML data', dest='formatter', action='store_const', const=YamlWriter)

parser = argparse.ArgumentParser(prog='dbexport', parents=[parent])
parser.add_argument('uri', help="""the URI to parse (format for PostgreSQL: user@host/database/table/column=value; for SQLite: databasefile.db/table/column=value)""")
parser.add_argument('-i', '--include', help='include the specified columns and their foreign rows, if any (multiple columns can be specified by separating them with a comma)')
parser.add_argument('-x', '--exclude', help='Exclude the specified columns')
parser.add_argument('-m', '--limit', type=int, default=50, help='limit the results of the main query to this amount of rows')
parser.add_argument('-p', '--package', default='models', help='the package for YAML entities')

class RowItem():
    def __init__(self, row, exclude):
        self.row = row
        self.exclude = exclude
    def __hash__(self):
        return hash(self.row.autocomplete())
    def __eq__(self, o):
        return hash(self.row.autocomplete()) == hash(o.row.autocomplete())
    def format(self):
        Formatter.formatter.format_row(self.row)

def fk_by_a_table_name(fks):
    return dict(map(lambda (k, v): (v.a.table.name, v), fks.iteritems()))

def create_items(items, include, exclude):
    logger.debug('create_items(items=%s, include=%s, exclude=%s)', items, include, exclude)

    results_pre = []
    results_post = []
    includes = {}
    for item in items:
        for i in include:
            c = re.sub('([^\\.]*)\\..*', '\\1', i)
            fk = None
            for key, val in item.table.fks.iteritems():
                if val.a.table.name == c:
                    fk = val
                    break
            col = item.table.column(c)
            if not col and not fk:
                raise UnknownColumnException(item.table, i)
            if fk:
                fk.a.table.connection = item.table.connection
                if fk not in includes:
                    includes[fk] = []
                includes[fk].append(item[fk.b.name])
            if col and col.name in item.table.fks:
                fk = item.table.fks[col.name]
                fk.b.table.connection = item.table.connection
                if fk not in includes:
                    includes[fk] = []
                includes[fk].append(item[fk.a.name])
    if exclude:
        for item in items:
            for x in exclude:
                c = re.sub('([^\\.]*)\\..*', '\\1', x)
                fks = fk_by_a_table_name(item.table.fks)
                if c in fks:
                    fk = fks[c]
                col = item.table.column(c)
                if not col and not fk:
                    raise UnknownColumnException(item.table, x, fks.keys() + map(lambda c: c.name, item.table.cols))
            # only check first item, as we expect all items are from the same table
            break
    for fk in includes.keys():
        if fk.a.table.name == item.table.name:
            # forward references, must be in pre
            results_pre += create_items(
                fk.b.table.rows([QueryFilter(fk.b.name, 'in', includes[fk])], limit=-1),
                remove_prefix(fk.a.name, include),
                remove_prefix(fk.a.name, exclude))
        else:
            # backward reference, must be in post
            results_post += create_items(
                fk.a.table.rows([QueryFilter(fk.a.name, 'in', includes[fk])], limit=-1),
                remove_prefix(fk.a.table.name, include),
                remove_prefix(fk.a.table.name, exclude))
            
    return results_pre + map(lambda i: RowItem(i, exclude), items) + results_post

def prefix(s):
    return re.sub('([^\\.]*)\\..*', '\\1', s)

class DatabaseExporter:
    """The main class"""

    @staticmethod
    def export(options):
        """The main method that splits the arguments and starts the magic"""

        cons = Source.connections()

        # search exact match of connection
        for connection in cons:
            opts = options.get(connection.driver)
            if ((opts.show == 'values'
                or opts.show == 'columns' and opts.filter != None)
                and connection.matches(opts)):
                try:
                    connection.connect(opts.database)
                    tables = connection.tables()
                    if opts.table not in tables:
                        raise Exception("Could not find table '{0}'".format(opts.table))
                    table = tables[opts.table]
                    items = create_items(
                        table.rows(opts.filter, opts.limit),
                        opts.include,
                        opts.exclude)
                    # remove duplicates
                    return list(OrderedDict.fromkeys(items))
                finally:
                    connection.close()

        raise Exception('Specify the complete URI to a table')

def main():
    try:
        print Writer.write(run(sys.argv))
    except SystemExit, e:
        sys.exit(-1)
    except BaseException, e:
        sys.stderr.write('{0}: {1}\n'.format(sys.argv[0].split('/')[-1], e))
        raise

def run(argv):
    options = Config.init(argv, parser)

    if options.formatter:
        Writer.set(options.formatter(options))
    else:
        Writer.set(SqlInsertWriter())

    try:
        return DatabaseExporter.export(options)
    except BaseException, e:
        logger.exception(e)
        raise

if __name__ == "__main__":
    main()
