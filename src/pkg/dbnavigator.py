#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import time

from .options import *
from .model.column import *
from .model.row import *
from .querybuilder import QueryBuilder
from .printer import *
from .sources import *
from .item import Item
from .logger import logduration

from .postgresql import *
from .sqlite import *
from .mock import *

VALID = "yes"
INVALID = "no"

IMAGE_CONNECTION = 'images/connection.png'
IMAGE_DATABASE = 'images/database.png'
IMAGE_TABLE = 'images/table.png'
IMAGE_ROW = 'images/row.png'
IMAGE_VALUE = 'images/value.png'
IMAGE_FOREIGN_KEY = 'images/foreign-key.png'
IMAGE_FOREIGN_VALUE = 'images/foreign-value.png'

OPTION_URI_TABLES_FORMAT = '%s/%s/'
OPTION_URI_ROW_FORMAT = '%s/%s/%s'

logger = logging.getLogger(__name__)

def strip(s):
    if type(s) == str:
        return s.strip()
    return s

def tostring(key):
    if isinstance(key, unicode):
        return key.encode('ascii', errors='ignore')
    return key

class DatabaseNavigator:
    """The main class"""

    @staticmethod
    def main(args=[]):
        """The main method that splits the arguments and starts the magic"""

        Options.init(args)

        connections = Source.connections()
        con = None

        # search exact match of connection
        if Options.uri:
            for connection in connections:
                if connection.matches(Options):
                    connection.proceed()
                    return

        if Options.database == None:
            # print all connections
            cons = [c for c in connections if c.filter(Options)]
            DatabaseNavigator.print_connections(cons)
            return

        Printer.write([])

    @staticmethod
    def print_connections(cons):
        """Prints the given connections %s"""

        logger.debug(DatabaseNavigator.print_connections.__doc__, cons)
        Printer.write([Item(c.title(), c.subtitle(), c.autocomplete(), VALID, IMAGE_CONNECTION) for c in cons])

    @staticmethod
    def print_databases(dbs):
        """Prints the given databases %s"""

        logger.debug(DatabaseNavigator.print_databases.__doc__, dbs)

        Printer.write([Item(database.autocomplete(), 'Database', database.autocomplete(), VALID, IMAGE_DATABASE) for database in dbs])

    @staticmethod
    def print_tables(tables):
        """Prints the given tables %s"""

        logger.debug(DatabaseNavigator.print_tables.__doc__, tables)

        Printer.write([Item(t.name, 'Title: %s' % t.comment.title, OPTION_URI_TABLES_FORMAT % (t.uri, t), VALID, IMAGE_TABLE) for t in tables])

    @staticmethod
    def print_rows(rows):
        """Prints the given rows"""

        logger.debug(DatabaseNavigator.print_rows.__doc__)

        def val(row, column):
            colname = '%s_title' % column
            if colname in row.row:
                return '%s (%s)' % (row.row[colname], row.row[column])
            return row.row[column]

        def pk(row): return row.table.primary_key

        Printer.write([Item(val(row, 'title'), val(row, 'subtitle'), row.table.autocomplete(pk(row), row[pk(row)]), VALID, IMAGE_ROW) for row in rows])

    @staticmethod
    def print_values(connection, table, filter):
        """Prints the given row values according to the given filter"""

        logger.debug(DatabaseNavigator.print_values.__doc__)

        foreign_keys = table.fks
        query = QueryBuilder(connection, table, filter=filter, limit=1).build()
        result = connection.execute(query, 'Values')
        
        row = Row(connection, table, result.fetchone())

        logger.debug('Comment.display: %s', table.comment.display)
        if table.comment.display:
            keys = table.comment.display
        else:
            keys = sorted(row.row.keys(), key=lambda key: '' if key == COMMENT_TITLE else tostring(key))

        if 'subtitle' not in keys:
            keys.insert(0, 'subtitle')
        if 'title' not in keys:
            keys.insert(0, 'title')

        def fkey(column): return foreign_keys[column.name] if column.name in foreign_keys else column

        def val(row, column):
            colname = '%s_title' % column
            if colname in row.row:
                return '%s (%s)' % (row.row[colname], row.row[column])
            return row.row[tostring(column)]

        items = []
        for key in keys:
            autocomplete = table.autocomplete(key, row.row[tostring(key)])
            value = val(row, key)
            f = fkey(Column(table, key))
            icon = IMAGE_VALUE
            if f.__class__.__name__ == 'ForeignKey':
                icon = IMAGE_FOREIGN_KEY
            items.append(Item(value, f, autocomplete, VALID, icon))

        for key in sorted(foreign_keys, key=lambda k: foreign_keys[k].a.table.name):
            fk = foreign_keys[key]
            if fk.b.table.name == table.name:
                autocomplete = fk.a.table.autocomplete(fk.b.name, "{0}={1}".format(fk.a.name, row.row[fk.b.name]), OPTION_URI_ROW_FORMAT)
                colname = fk.a.name
                f = fkey(Column(fk.a.table, fk.a.name))
                items.append(Item('Ref: %s' % fk.a, f, autocomplete, INVALID, IMAGE_FOREIGN_VALUE))

        Printer.write(items)

if __name__ == "__main__":
    import sys
    import os

    loglevel = logging.WARNING

    loglevel_env = os.getenv("LOGLEVEL")
    if loglevel_env:
        numeric_level = getattr(logging, loglevel_env.upper(), None)
        if not isinstance(numeric_level, int):
            raise ValueError('Invalid log level: %s' % loglevel_env)
        loglevel = numeric_level

    logging.basicConfig(filename='/tmp/dbexplorer.log', level=loglevel)
    
    logger.debug("""
###
### Called with args: %s ###
###""", sys.argv)

    try:
        DatabaseNavigator.main(sys.argv)
    except BaseException, e:
        logger.exception(e)
        Printer.write([Item(str(e), type(e), '', INVALID, '')])
