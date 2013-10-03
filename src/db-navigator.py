#!/usr/local/bin/python
# -*- coding: utf-8 -*-

import logging
import pprint
import psycopg2
import psycopg2.extras
import json
import sys
from os.path import expanduser
from urlparse import urlparse

ITEMS_FORMAT = '<items>{0}</items>'
ITEM_FORMAT = """
    <item uid="{0}" arg="{2}" autocomplete="{1}">
        <title>{2}</title>
        <subtitle>{3}</subtitle>
        <icon>images/{4}</icon>
    </item>
"""

OPTION_URI_FORMAT = '%s@%s/%s'
OPTION_URI_DATABASE_FORMAT = '%s/'
OPTION_URI_TABLES_FORMAT = '%s/%s/'
OPTION_URI_VALUE_FORMAT = '%s/%s/%s/'

COMMENT_ID = 'id'
COMMENT_TITLE = 'title'
COMMENT_SUBTITLE = 'subtitle'
COMMENT_ORDER_BY = 'order'
COMMENT_SEARCH = 'search'
COMMENT_DISPLAY = 'display'

JOIN_FORMAT = """
        left outer join \"{0}\" on \"{0}\".{1} = \"{2}\".{3}"""
TABLE_PROJECTION_FORMAT = '%s as id, %s as title, %s as subtitle'
TABLE_WHERE_FORMAT = "%s ilike '%%%s%%' or %s ilike '%%%s%%' or %s || '' = '%s'"
TABLE_QUERY_FORMAT = """
select
        %s
    from
        "%s"
    where
        %s
    %s
    limit 20
"""
TABLE_ORDER_BY = 'order by %s'

DATABASES_QUERY = """
select
        datname as database_name
    from
        pg_database
    where
        datistemplate = false
    order by datname
"""
FOREIGN_KEY_QUERY_FORMAT = """
select
        tc.constraint_name,
        tc.table_name,
        kcu.column_name,
        ccu.table_name foreign_table_name,
        ccu.column_name foreign_column_name
    from
        information_schema.table_constraints tc
        join information_schema.key_column_usage kcu ON tc.constraint_name = kcu.constraint_name
        join information_schema.constraint_column_usage ccu ON ccu.constraint_name = tc.constraint_name
    where
        constraint_type = 'FOREIGN KEY'
         and tc.table_name = '%s'
"""
ROW_QUERY_FORMAT = """
select
        column_name
    from
        INFORMATION_SCHEMA.COLUMNS
    where
        table_name = '%s'
"""
TABLES_QUERY = """
select
        t.table_name as tbl, obj_description(c.oid) as comment
    from information_schema.tables t,
        pg_class c
    where
        table_schema = 'public'
        and t.table_name = c.relname
        and c.relkind = 'r'
    order by t.table_name
"""
VALUES_QUERY_FORMAT = """
select
        \"{0}\".* {1}
    from
        \"{0}\" {2}
    where
        {3} = '{4}'
"""

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
        self.print_items([[c, c, c, 'Connection', 'connection.png'] for c in cons])

    def print_databases(self, db, dbs, options):
        """Prints the given databases according to the given filter"""

        logging.debug(self.print_databases.__doc__)
        if options.user:
            dbs = [db for db in dbs if options.user in db.connection.user]
        if options.host:
            dbs = [db for db in dbs if options.host in db.connection.host]
        if options.database:
            dbs = [db for db in dbs if options.database in db.name]

        self.print_items([[database, database.autocomplete(), database, 'Database', 'database.png'] for database in dbs])

    def print_tables(self, tables, filter):
        """Prints the given tables according to the given filter"""

        logging.debug(self.print_tables.__doc__)
        if filter:
            tables = [t for t in tables if t.name.startswith(filter)]
        self.print_items([[t.name, OPTION_URI_TABLES_FORMAT % (t.uri(), t), t.name, 'Title: %s' % t.comment[COMMENT_TITLE], 'table.png'] for t in tables])

    def print_rows(self, table, filter):
        """Prints the given rows according to the given filter"""

        logging.debug(self.print_rows.__doc__)
        rows = table.rows(filter)
        self.print_items([[row[0], row.table.autocomplete('id', row['id']), strip(row[1]), strip(row[2]), 'row.png'] for row in rows])

    def print_values(self, table, filter):
        """Prints the given row values according to the given filter"""

        logging.debug(self.print_values.__doc__)

        foreign_keys = table.foreign_keys()
        columns = ''
        joins = ''
        join_tables = []
        
        logging.debug('Foreign keys: %s' % ', '.join(foreign_keys))
        for key in foreign_keys.keys():
            fk = foreign_keys[key]
            title = fk.b.table.comment[COMMENT_TITLE]
            if title != '*':
                columns += ', {0} {1}_title'.format(title, fk.a.name)
            if fk.b.table.name not in join_tables:
                joins += JOIN_FORMAT.format(fk.b.table.name, fk.b.name, fk.a.table.name, fk.a.name)
                join_tables.append(fk.b.table.name)

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

        query = VALUES_QUERY_FORMAT.format(table.name, columns, joins, table.comment[COMMENT_ID], filter)
        logging.debug('Query values: %s' % query)
        cur = table.connection.cursor()
        cur.execute(query)
        row = Row(table.connection, table, cur.fetchone())

        if row.row:
            self.print_items([[key, table.autocomplete(key, row.row[key]), val(row, key), fk(Column(table, key)), 'value.png'] for key in keys])
        else:
            self.print_items([])

class Database:
    """The database used with the given connection"""

    def __init__(self, connection, name):
        self.connection = connection
        self.name = name

    def __repr__(self):
        return "%s@%s/%s" % (self.connection.user, self.connection.host, self.name)

    def autocomplete(self):
        """Retrieves the autocomplete string"""

        return OPTION_URI_DATABASE_FORMAT % (self.__repr__())

class TableComment:
    """The comment on the given table that allows to display much more accurate information"""

    def __init__(self, table, json_string):
        id = "\"%s\".id" % table.name
        self.d = {COMMENT_TITLE: '*', COMMENT_ORDER_BY: ['title'], COMMENT_SEARCH: [], COMMENT_DISPLAY: []}
        self.d[COMMENT_SUBTITLE] = "'Id: ' || %s" % id
        self.d[COMMENT_ID] = id

        if json_string:
            try:
                self.d = dict(self.d.items() + json.loads(json_string).items())
            except TypeError, e:
                pass

    def __getitem__(self, i):
        return self.d[i]

    def __repr__(self):
        return self.d.__repr__()

class Table:
    def __init__(self, connection, database, name, comment):
        self.connection = connection
        self.database = database
        self.name = name
        self.comment = TableComment(self, comment)
        self.fks = None

    def __repr__(self):
        return self.name

    def uri(self):
        """Creates the URI for this table"""

        return '%s@%s/%s' % (self.connection.user, self.connection.host, self.database)

    def autocomplete(self, column, value):
        """Retrieves the autocomplete string for the given column and value"""

        tablename = self.name
        fks = self.foreign_keys()
        if column in fks:
            fk = fks[column]
            tablename = fk.b.table.name

        return OPTION_URI_VALUE_FORMAT % (self.uri(), tablename, value)

    def create_query(self, filter):
        """Creates the query from the given parameters"""

        projection = '*'
        order_by = ''
        where = 'true=true'

        if self.comment[COMMENT_TITLE] != '*':
            projection = TABLE_PROJECTION_FORMAT % (self.comment[COMMENT_ID], self.comment[COMMENT_TITLE], self.comment[COMMENT_SUBTITLE])
        if projection != '*' and self.comment[COMMENT_ORDER_BY]:
            order_by = TABLE_ORDER_BY % ', '.join(self.comment[COMMENT_ORDER_BY])
        if filter:
            if self.comment[COMMENT_SEARCH]:
                conjunctions = []
                for search_field in self.comment[COMMENT_SEARCH]:
                    conjunctions.append("%s ilike '%%%s%%'" % (search_field, filter))
                conjunctions.append("%s || '' = '%s'" % (self.comment[COMMENT_ID], filter))
                where = ' or '.join(conjunctions)
            elif self.comment[COMMENT_TITLE] != '*':
                where = TABLE_WHERE_FORMAT % (self.comment[COMMENT_TITLE], filter, self.comment[COMMENT_SUBTITLE], filter, self.comment[COMMENT_ID], filter)

        query = TABLE_QUERY_FORMAT % (projection, self.name, where, order_by)
        return query

    def rows(self, filter):
        """Retrieves rows from the table with the given filter applied"""

        query = self.create_query(filter)
        logging.debug('Query rows: %s' % query)
        cur = self.connection.cursor()
        cur.execute(query)

        def t(row): return Row(self.connection, self, row)

        return map(t, cur.fetchall())

    def foreign_keys(self):
        """Retrieves the foreign keys of the table"""

        if not self.fks:
            logging.debug('Retrieve foreign keys')
            query = FOREIGN_KEY_QUERY_FORMAT % self.name
            logging.debug('Query foreign keys: %s' % query)
            cur = self.connection.cursor()
            cur.execute(query)
            self.fks = {}
            for row in cur.fetchall():
                self.fks[row['column_name']] = ForeignKey(Column(self.connection.table_map[row['table_name']], row['column_name']), Column(self.connection.table_map[row['foreign_table_name']], row['foreign_column_name']))

        return self.fks

class Row:
    """A table row from the database"""

    def __init__(self, connection, table, row):
        self.connection = connection
        self.table = table
        self.row = row

    def __getitem__(self, i):
        return self.row[i]

    def values(self):
        return self.row

class Column:
    """A table column"""

    def __init__(self, table, name):
        self.table = table
        self.name = name

    def __repr__(self):
        return '%s.%s' % (self.table.name, self.name)

class ForeignKey:
    """A foreign key connection between the originating column a and the foreign column b"""

    def __init__(self, a, b):
        self.a = a
        self.b = b

    def __repr__(self):
        return '%s -> %s' % (self.a, self.b)

class DatabaseConnection:
    """A database connection"""

    def __init__(self, line):
        (self.host, self.port, self.database, self.user, self.password) = line.split(':')
        self.con = None
        self.dbs = None
        self.tbls = None

    def __repr__(self):
        return '%s@%s/%s' % (self.user, self.host, self.database if self.database != '*' else '')

    def __str__(self):
        return self.__repr__();

    def matches(self, s):
        return s.startswith("%s@%s" % (self.user, self.host))

    def connect(self, database):
        logging.debug('Connecting to database %s' % database)
        
        if database:
            try:
                self.con = psycopg2.connect(host=self.host, database=database, user=self.user, password=self.password)
            except psycopg2.DatabaseError, e:
                self.con = psycopg2.connect(host=self.host, user=self.user, password=self.password)
        else:
            self.con = psycopg2.connect(host=self.host, user=self.user, password=self.password)
        self.table_map = {t.name: t for t in self.tables(database)}

    def cursor(self):
        return self.con.cursor(cursor_factory=psycopg2.extras.DictCursor)

    def databases(self):
        if not self.dbs:
            query = DATABASES_QUERY
            logging.debug('Query databases: %s' % query)

            cur = self.cursor()
            cur.execute(query)
    
            def d(row): return Database(self, row[0])
    
            self.dbs = map(d, cur.fetchall())
        
        return self.dbs

    def tables(self, database):
        if not self.tbls:
            query = TABLES_QUERY
            logging.debug('Query tables: %s' % query)
    
            cur = self.cursor()
            cur.execute(query)
    
            def t(row): return Table(self, database, row[0], row[1])
    
            self.tbls = map(t, cur.fetchall())

        return self.tbls

DatabaseNavigator().main()
