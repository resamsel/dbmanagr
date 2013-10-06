#!/usr/local/bin/python
# -*- coding: utf-8 -*-

import logging
import sys
from os.path import expanduser
from urlparse import urlparse

from const import *
from model import *
from querybuilder import QueryBuilder

logging.basicConfig(filename='/tmp/dbexplorer.log', level=logging.DEBUG)

logging.debug("""
###
### Called with args: %s ###
###""", sys.argv)

def strip(s):
    if type(s) == str:
        return s.strip()
    return s
def html_escape(s):
    if type(s) == str:
        return s.replace('&', '&amp;').replace('"', '&quot;').replace('<', '&lt;')
    return s

class Options:
    def __init__(self, args):
        self.user = None
        self.host = None
        self.database = None
        self.table = None
        self.filter = None
        self.display = False

        if len(args) > 1:
            arg = args[1]
            if '@' not in arg:
                arg += '@'
            url = urlparse('postgres://%s' % arg)
            locs = url.netloc.split('@')
            paths = url.path.split('/')

            if len(locs) > 0:  self.user = locs[0]
            if len(locs) > 1:  self.host = locs[1]
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

        connections = []
        pgpass = None
        con = None
        options = Options(sys.argv)
        theconnection = None

        with open(expanduser('~/.pgpass')) as f:
            pgpass = f.readlines()

        for line in pgpass:
            connection = DatabaseConnection(line.strip())
            logging.debug('Database Connection: %s' % connection)
            connections.append(connection)

        logging.debug('Options.uri(): %s' % options.uri())
        if options.uri():
            for connection in connections:
                if connection.matches(options.uri()):
                    theconnection = connection
                    break

        if not theconnection:
            self.print_connections(connections, options)
            return

        try:
            theconnection.connect(options.database)

            # look for databases if needed
            databases = theconnection.databases()
#            logging.debug('Databases: %s' % ', '.join([db.__repr__() for db in databases]))
            if not options.database or options.table == None:
                self.print_databases(theconnection, databases, options)
                return

            tables = [t for k, t in theconnection.table_map.iteritems()]
            tables = sorted(tables, key=lambda t: t.name)
            if options.table:
                ts = [t for t in tables if options.table == t.name]
                if len(ts) == 1 and options.filter != None:
                    table = ts[0]
                    if options.filter and options.display:
                        self.print_values(table, options.filter)
                    else:
                        self.print_rows(table, options.filter)
                    return
            
            self.print_tables(tables, options.table)
        except psycopg2.DatabaseError, e:
            logging.error('Error %s' % e)
            sys.exit(1)
        finally:
            if theconnection and theconnection.con:
                theconnection.con.close()
    def print_items(self, items):
        """Prints the given items according to the ITEM_FORMAT"""

        print ITEMS_FORMAT.format(''.join([ITEM_FORMAT.format(*map(html_escape, i)) for i in items]))

    def print_connections(self, connections, options):
        """Prints the given connections according to the given filter"""

        logging.debug('Printing connections')
        cons = connections
        if options.user:
            cons = [c for c in connections if options.user in c.__repr__()]
        self.print_items([[c, c, c, 'Connection', IMAGE_CONNECTION] for c in cons])

    def print_databases(self, db, dbs, options):
        """Prints the given databases according to the given filter"""

        logging.debug(self.print_databases.__doc__)
        if options.user:
            dbs = [db for db in dbs if options.user in db.connection.user]
        if options.host:
            dbs = [db for db in dbs if options.host in db.connection.host]
        if options.database:
            dbs = [db for db in dbs if options.database in db.name]

        self.print_items([[database, database.autocomplete(), database, 'Database', IMAGE_DATABASE] for database in dbs])

    def print_tables(self, tables, filter):
        """Prints the given tables according to the given filter"""

        logging.debug(self.print_tables.__doc__)
        if filter:
            tables = [t for t in tables if t.name.startswith(filter)]
        self.print_items([[t.name, OPTION_URI_TABLES_FORMAT % (t.uri(), t), t.name, 'Title: %s' % t.comment[COMMENT_TITLE], IMAGE_TABLE] for t in tables])

    def print_rows(self, table, filter):
        """Prints the given rows according to the given filter"""

        logging.debug(self.print_rows.__doc__)
        rows = table.rows(filter)

        def val(row, column):
            colname = '%s_title' % column
            if colname in row.row:
                return '%s (%s)' % (row.row[colname], row.row[column])
            return row.row[column]

        self.print_items([[row[0], table.autocomplete('id', row['id']), val(row, 'title'), strip(row[2]), IMAGE_ROW] for row in rows])

    def print_values(self, table, filter):
        """Prints the given row values according to the given filter"""

        logging.debug(self.print_values.__doc__)

        foreign_keys = table.foreign_keys()
        query = QueryBuilder(table, id=filter, limit=1).build()
        
        logging.debug('Query values: %s' % query)
        cur = table.connection.cursor()
        cur.execute(query)
        row = Row(table.connection, table, cur.fetchone())

        if table.comment[COMMENT_DISPLAY]:
            keys = table.comment[COMMENT_DISPLAY]
        else:
            keys = sorted(row.row.keys(), key=lambda key: '' if key == COMMENT_TITLE else key)

        def fk(column): return foreign_keys[column.name] if column.name in foreign_keys else column

        def val(row, column):
            colname = '%s_title' % column
            if colname in row.row:
                return '%s (%s)' % (row.row[colname], row.row[column])
            return row.row[column]

        if row.row:
            self.print_items([[key, table.autocomplete(key, row.row[key]), val(row, key), fk(Column(table, key)), IMAGE_VALUE] for key in keys])
        else:
            self.print_items([])

DatabaseNavigator().main()
