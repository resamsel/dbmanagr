#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import sys
import time
from urlparse import urlparse

from const import *
from model import *
from querybuilder import QueryBuilder
from printer import *
from sources import *
from item import Item
from logger import logduration

logging.basicConfig(filename='/tmp/dbexplorer.log', level=logging.DEBUG)

logging.debug("""
###
### Called with args: %s ###
###""", sys.argv)

def strip(s):
    if type(s) == str:
        return s.strip()
    return s

printers = {
    '-x': XmlPrinter(),
    '-s': SimplePrinter(),
    '-j': JsonPrinter(),
    '-p': Printer()
}

class Options:
    def __init__(self, args):
        self.user = None
        self.host = None
        self.database = None
        self.table = None
        self.filter = None
        self.display = False
        self.printer = printers['-x']

        if len(args) > 1 and args[1].startswith('-'):
            self.printer = printers[args[1]]
            del args[1]
            
        if len(args) > 1:
            arg = args[1]
            if '@' not in arg:
                arg += '@'
            url = urlparse('postgres://%s' % arg)
            locs = url.netloc.split('@')
            paths = url.path.split('/')

            if len(locs) > 0:  self.user = locs[0]
            if '@' in args[1]: self.host = locs[1]
            if len(paths) > 1: self.database = paths[1]
            if len(paths) > 2: self.table = paths[2]
            if len(paths) > 3: self.filter = paths[3]
            self.display = arg.endswith('/')
        
        logging.debug('Options: %s' % self)

    def uri(self):
        if self.user and self.host:
            return OPTION_URI_FORMAT % (self.user, self.host, self.table if self.table else '')
        return None

    def __repr__(self):
        return self.__dict__.__repr__()

class DatabaseNavigator:
    """The main class"""

    def main(self):
        """The main method that splits the arguments and starts the magic"""

        self.options = Options(sys.argv)

        connections = set(DBExplorerSource().list() + PgpassSource().list())
        pgpass = None
        con = None
        theconnection = None

        # search exact match of connection
        if self.options.uri():
            for connection in connections:
                if connection.matches(self.options.uri()):
                    theconnection = connection
                    break

        if self.options.database == None:
            # print all connections
            self.print_connections(connections)
            return

        try:
            theconnection.connect(self.options.database)

            if not self.options.database or self.options.table == None:
                self.print_databases(theconnection, theconnection.databases(), self.options.database)
                return

            tables = [t for k, t in theconnection.table_map.iteritems()]
            tables = sorted(tables, key=lambda t: t.name)
            if self.options.table:
                ts = [t for t in tables if self.options.table == t.name]
                if len(ts) == 1 and self.options.filter != None:
                    table = ts[0]
                    if self.options.filter and self.options.display:
                        self.print_values(table, self.options.filter)
                    else:
                        self.print_rows(table, self.options.filter)
                    return
            
            self.print_tables(tables, self.options.table)
        except psycopg2.DatabaseError, e:
            logging.error('Error %s' % e)
            sys.exit(1)
        finally:
            if theconnection and theconnection.con:
                theconnection.con.close()
    def print_items(self, items):
        """Prints the given items according to the ITEM_FORMAT"""

        self.options.printer.write(items)

    def print_connections(self, connections):
        """Prints the given connections {connections}"""

        logging.debug(self.print_connections.__doc__.format(connections=connections))
        cons = connections
        if self.options.user:
            filter = self.options.user
            if self.options.host != None:
                cons = [c for c in cons if filter in c.user]
                logging.debug('self.options.host: %s' % cons)
            else:
                cons = [c for c in cons if filter in c.user or filter in c.host]
                logging.debug('not self.options.host: %s' % cons)
        if self.options.host != None:
            cons = [c for c in cons if self.options.host in c.host]
            logging.debug('self.options.host != None: %s' % cons)
        self.print_items([Item(c.autocomplete(), 'Connection', c.autocomplete(), VALID, IMAGE_CONNECTION) for c in cons])

    def print_databases(self, database, dbs, filter=None):
        """Prints the given databases {dbs} according to the given filter {filter}"""

        logging.debug(self.print_databases.__doc__.format(database=database, dbs=dbs, filter=filter))

        if filter:
            dbs = [db for db in dbs if filter in db.name]

        self.print_items([Item(database.autocomplete(), 'Database', database.autocomplete(), VALID, IMAGE_DATABASE) for database in dbs])

    def print_tables(self, tables, filter):
        """Prints the given tables according to the given filter"""

        logging.debug(self.print_tables.__doc__)
        if filter:
            tables = [t for t in tables if t.name.startswith(filter)]
        self.print_items([Item(t.name, 'Title: %s' % t.comment.title, OPTION_URI_TABLES_FORMAT % (t.uri(), t), VALID, IMAGE_TABLE) for t in tables])

    def print_rows(self, table, filter):
        """Prints the given rows according to the given filter"""

        logging.debug(self.print_rows.__doc__)
        rows = table.rows(filter)

        def val(row, column):
            colname = '%s_title' % column
            if colname in row.row:
                return '%s (%s)' % (row.row[colname], row.row[column])
            return row.row[column]

        self.print_items([Item(val(row, 'title'), val(row, 'subtitle'), table.autocomplete('id', row['id']), VALID, IMAGE_ROW) for row in rows])

    def print_values(self, table, filter):
        """Prints the given row values according to the given filter"""

        logging.debug(self.print_values.__doc__)

        foreign_keys = table.fks
        query = QueryBuilder(table, id=filter, limit=1).build()
        
        logging.debug('Query values: %s' % query)
        cur = table.connection.cursor()
        start = time.time()
        cur.execute(query)
        logduration('Query values', start)
        row = Row(table.connection, table, cur.fetchone())

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

        self.print_items(items)

try:
    DatabaseNavigator().main()
except BaseException, e:
    logging.exception(e)
