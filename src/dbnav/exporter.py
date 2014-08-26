#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import time
import sys
import argparse
import re

from .config import Config
from .item import Item, INVALID
from .writer import Writer, StdoutWriter
from .sources import Source
from .logger import logger, logduration
from dbnav.utils import remove_prefix
from dbnav.querybuilder import QueryFilter
from dbnav.model.databaseconnection import values

parser = argparse.ArgumentParser(prog='dbexport')
parser.add_argument('uri', help="""The URI to parse. Format for PostgreSQL: user@host/database/table/column=value; for SQLite: databasefile.db/table/column=value""")
group = parser.add_mutually_exclusive_group()
group.add_argument('-d', '--default', default=True, help='Output format: SQL insert into statements', action='store_true')
parser.add_argument('-i', '--include', help='Include the specified columns and their foreign rows, if any. Multiple columns can be specified by separating them with a comma (,)')
parser.add_argument('-x', '--exclude', help='Exclude the specified columns')
parser.add_argument('-m', '--limit', type=int, default=50, help='Limit the results of the main query to this amount of rows')
parser.add_argument('-f', '--logfile', default='/tmp/dbnavigator.log', help='the file to log to')
parser.add_argument('-l', '--loglevel', default='warning', help='the minimum level to log')

def create_columns(row, exclude):
    return u','.join([col.name for col in row.table.cols if col.name not in exclude])

def create_values(row, exclude):
    table = row.table
    return u','.join([table.connection.format_value(col, row[col.name]) for col in table.cols if col.name not in exclude])

def create_item(row, exclude):
    table = row.table
    return Item('', u'insert into {table} ({columns}) values ({values});'.format(table=table.connection.escape_keyword(table.name), columns=create_columns(row, exclude), values=create_values(row, exclude)), '', '', '', '')

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
                raise Exception("Include column '{0}' or foreign key '{0}' does not exist in table '{1}'".format(i, item.table.name))
            if fk:
                fk.a.table.connection = item.table.connection
                if fk not in includes:
                    includes[fk] = []
                includes[fk].append(item[fk.b.name])
            if col:
                fk = item.table.fks[col.name]
                fk.b.table.connection = item.table.connection
                if fk not in includes:
                    includes[fk] = []
                includes[fk].append(item[fk.a.name])
    if exclude:
        for item in items:
            for x in exclude:
                c = re.sub('([^\\.]*)\\..*', '\\1', x)
                for key, val in item.table.fks.iteritems():
                    if val.a.table.name == c:
                        fk = val
                        break
                col = item.table.column(c)
                if not col and not fk:
                    raise Exception("Exclude column '{0}' or foreign key '{0}' does not exist in table '{1}'".format(i, item.table.name))
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
            
    return results_pre + [create_item(item, exclude) for item in items] + results_post

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
                    table = connection.tables()[opts.table]
                    return create_items(
                        table.rows(opts.filter, opts.limit),
                        opts.include,
                        opts.exclude)
                finally:
                    connection.close()

        raise Exception('Specify the complete URI to a table')

def main():
    print Writer.write(run(sys.argv))

def run(argv):
    options = Config.init(argv, parser)
    options.artificial_projection = False
    if options.default:
        Writer.set(StdoutWriter(u'{0}', u'{title}'))

    try:
        return DatabaseExporter.export(options)
    except BaseException, e:
        logger.exception(e)
        raise

if __name__ == "__main__":
    main()
