#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import time

from .options import *
from .model.column import *
from .model.row import *
from .querybuilder import QueryBuilder
from .writer import *
from .sources import *
from .item import Item
from .logger import logduration

from .postgresql import *
from .sqlite import *

VALID = "yes"
INVALID = "no"

IMAGE_CONNECTION = 'images/connection.png'
IMAGE_DATABASE = 'images/database.png'
IMAGE_TABLE = 'images/table.png'
IMAGE_VALUE = 'images/value.png'
IMAGE_FOREIGN_KEY = 'images/foreign-key.png'
IMAGE_FOREIGN_VALUE = 'images/foreign-value.png'

OPTION_URI_TABLES_FORMAT = '%s%s/'
OPTION_URI_ROW_FORMAT = '%s%s/%s'

logger = logging.getLogger(__name__)

def strip(s):
    if type(s) == str:
        return s.strip()
    return s

def tostring(key):
    if isinstance(key, unicode):
        return key.encode('ascii', errors='ignore')
    return key

def create_connections(cons):
    """Creates connection items"""

    return [c.item() for c in cons]

def create_databases(dbs):
    """Creates database items"""

    return [database.item() for database in dbs]

def create_tables(tables):
    """Creates table items"""

    return [t.item() for t in tables]

def create_columns(columns):
    """Creates column items"""

    return [c.item() for c in columns]

def create_rows(rows):
    """Creates row items"""

    logger.debug('create_rows(rows=%s)', rows)

    return [row.item() for row in rows]

def create_values(connection, table, filter):
    """Creates row values according to the given filter"""
    
    logger.debug('create_values(connection=%s, table=%s, filter=%s)', connection, table, filter)

    foreign_keys = table.fks
    logger.debug('QueryBuilder(connection=%s, table=%s, filter=%s, limit=1)',
        connection, table, filter)
    query = QueryBuilder(connection, table, filter=filter, order=[], limit=1).build()
    result = connection.execute(query, 'Values')
        
    row = Row(connection, table, result.fetchone())

    logger.debug('Comment.display: %s', table.comment.display)
    if table.comment.display:
        keys = table.comment.display
    else:
        keys = sorted(row.row.keys(), key=lambda key: '' if key == COMMENT_TITLE else tostring(key))

    def fkey(column): return foreign_keys[column.name] if column.name in foreign_keys else column

    def val(row, column):
        colname = '%s_title' % column
        if colname in row.row:
            return '%s (%s)' % (row.row[colname], row.row[column])
        return row.row[tostring(column)]

    items = []
    for key in keys:
        value = val(row, key)
        if key in table.fks:
            # if key is a foreign key column
            fk = table.fks[key]
            autocomplete = fk.b.table.autocomplete(fk.b.name, row.row[tostring(key)])
        else:
            autocomplete = table.autocomplete(key, row.row[tostring(key)], OPTION_URI_ROW_FORMAT)
        f = fkey(Column(table, key))
        icon = IMAGE_VALUE
        if f.__class__.__name__ == 'ForeignKey':
            icon = IMAGE_FOREIGN_KEY
        items.append(Item(value, f, autocomplete, VALID, icon))

    for key in sorted(foreign_keys, key=lambda k: foreign_keys[k].a.table.name):
        fk = foreign_keys[key]
        if fk.b.table.name == table.name:
            autocomplete = fk.a.table.autocomplete(fk.a.name, row.row[fk.b.name], OPTION_URI_ROW_FORMAT)
            logger.debug('table.name=%s, fk=%s, autocomplete=%s', table.name, fk, autocomplete)
            colname = fk.a.name
            f = fkey(Column(fk.a.table, fk.a.name))
            items.append(
                Item('Ref: %s' % fk.a,
                    f,
                    autocomplete,
                    INVALID,
                    IMAGE_FOREIGN_VALUE))

    return items

class DatabaseNavigator:
    """The main class"""

    @staticmethod
    def main(options):
        """The main method that splits the arguments and starts the magic"""

        cons = Source.connections()

        # search exact match of connection
        for connection in cons:
            opts = options.get(connection.driver)
            if opts.show != 'connections' and connection.matches(opts):
                return connection.proceed(opts)

        # print all connections
        return create_connections(sorted([c for c in cons if c.filter(options)], key=lambda c: c.title().lower()))

def main():
    Writer.write(run(sys.argv))

def run(argv):
    options = Options(argv)

    logging.basicConfig(filename=options.logfile,
        level=options.loglevel,
        format="%(asctime)s %(levelname)s %(filename)s:%(lineno)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S")
    
    logger.info("""
###
### Called with args: %s
###""", options.argv)
    logger.debug("Options: %s", options)

    try:
        return DatabaseNavigator.main(options)
    except BaseException, e:
        logger.exception(e)
        return [Item(str(e), type(e), '', INVALID, '')]

if __name__ == "__main__":
    main()
