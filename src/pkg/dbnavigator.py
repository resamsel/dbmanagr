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


def strip(s):
    if type(s) == str:
        return s.strip()
    return s

class DatabaseNavigator:
    """The main class"""

    def main(self, args=[]):
        """The main method that splits the arguments and starts the magic"""

        Options.init(args)

        connections = Source.connections()
        con = None

        # search exact match of connection
        if Options.uri:
            for connection in connections:
                if connection.matches(Options.uri):
                    con = connection
                    break

        if Options.database == None:
            # print all connections
            self.print_connections(connections)
            return

        try:
            if con == None:
                Printer.write([])
                return

            con.connect(Options.database)

            if not Options.database or Options.table == None:
                self.print_databases(con, con.databases(), Options.database)
                return

            tables = [t for k, t in con.tables().iteritems()]
            tables = sorted(tables, key=lambda t: t.name)
            if Options.table:
                ts = [t for t in tables if Options.table == t.name]
                if len(ts) == 1 and Options.filter != None:
                    table = ts[0]
                    if Options.filter and Options.display:
                        self.print_values(con, table, Options.filter)
                    else:
                        self.print_rows(con, table, Options.filter)
                    return
            
            self.print_tables(tables, Options.table)
        finally:
            if con and con.connected():
                con.close()
    def print_connections(self, connections):
        """Prints the given connections {connections}"""

        logging.debug(self.print_connections.__doc__.format(connections=connections))
        cons = connections
        if Options.user:
            filter = Options.user
            if Options.host != None:
                cons = [c for c in cons if filter in c.user]
                logging.debug('Options.host: %s' % cons)
            else:
                cons = [c for c in cons if filter in c.user or filter in c.host]
                logging.debug('not Options.host: %s' % cons)
        if Options.host != None:
            cons = [c for c in cons if Options.host in c.host]
            logging.debug('Options.host != None: %s' % cons)
        Printer.write([Item(c.title(), c.subtitle(), c.autocomplete(), VALID, IMAGE_CONNECTION) for c in cons])

    def print_databases(self, database, dbs, filter=None):
        """Prints the given databases {dbs} according to the given filter {filter}"""

        logging.debug(self.print_databases.__doc__.format(database=database, dbs=dbs, filter=filter))

        if filter:
            dbs = [db for db in dbs if filter in db.name]

        Printer.write([Item(database.autocomplete(), 'Database', database.autocomplete(), VALID, IMAGE_DATABASE) for database in dbs])

    def print_tables(self, tables, filter):
        """Prints the given tables according to the given filter"""

        logging.debug(self.print_tables.__doc__)
        if filter:
            tables = [t for t in tables if t.name.startswith(filter)]
        Printer.write([Item(t.name, 'Title: %s' % t.comment.title, OPTION_URI_TABLES_FORMAT % (t.uri, t), VALID, IMAGE_TABLE) for t in tables])

    def print_rows(self, connection, table, filter):
        """Prints the given rows according to the given filter"""

        logging.debug(self.print_rows.__doc__)
        rows = table.rows(connection, filter)

        def val(row, column):
            colname = '%s_title' % column
            if colname in row.row:
                return '%s (%s)' % (row.row[colname], row.row[column])
            return row.row[column]

        Printer.write([Item(val(row, 'title'), val(row, 'subtitle'), table.autocomplete('id', row['id']), VALID, IMAGE_ROW) for row in rows])

    def print_values(self, connection, table, filter):
        """Prints the given row values according to the given filter"""

        logging.debug(self.print_values.__doc__)

        foreign_keys = table.fks
        query = QueryBuilder(connection, table, filter=filter, limit=1).build()
        
        logging.debug('Query values: %s' % query)
        cur = connection.cursor()
        start = time.time()
        cur.execute(query)
        logduration('Query values', start)
        row = Row(connection, table, cur.fetchone())

        logging.debug('Comment.display: %s' % table.comment.display)
        if table.comment.display:
            keys = table.comment.display
        else:
            keys = sorted(row.row.keys(), key=lambda key: '' if key == COMMENT_TITLE else key)

        if 'subtitle' not in keys:
            keys.insert(0, 'subtitle')
        if 'title' not in keys:
            keys.insert(0, 'title')

        def fkey(column): return foreign_keys[column.name] if column.name in foreign_keys else column

        def val(row, column):
            colname = '%s_title' % column
            if colname in row.row:
                return '%s (%s)' % (row.row[colname], row.row[column])
            return row.row[column]

        items = []
        for key in keys:
            autocomplete = table.autocomplete(key, row.row[key])
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
    import logging

    logging.basicConfig(filename='/tmp/dbexplorer.log', level=logging.DEBUG)

    logging.debug("""
###
### Called with args: %s ###
###""", sys.argv)

    try:
        DatabaseNavigator().main(sys.argv)
    except BaseException, e:
        logging.exception(e)
        Printer.write([Item(str(e), type(e), '', INVALID, '')])
