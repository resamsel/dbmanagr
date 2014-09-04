#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import sys
import argparse
import sqlparse

from dbnav import wrapper
from dbnav.config import Config
from dbnav.writer import Writer, TestWriter
from dbnav.sources import Source
from dbnav.logger import logger, logduration
from dbnav.model.table import Table
from dbnav.utils import prefixes, remove_prefix
from dbnav.querybuilder import QueryFilter
from dbnav.args import parent_parser, format_group

from .writer import ExecuteWriter, SqlInsertWriter, ExecuteTestWriter

parent = parent_parser()

group = format_group(parent, ExecuteTestWriter)
group.add_argument('-d', '--default', help='output format: tuples', dest='formatter', action='store_const', const=ExecuteWriter)
group.add_argument('-I', '--insert', help='output format: SQL insert statements', dest='formatter', action='store_const', const=SqlInsertWriter)

parser = argparse.ArgumentParser(prog='dbexec', parents=[parent])
parser.add_argument('uri', help="""the URI to parse (format for PostgreSQL: user@host/database; for SQLite: databasefile.db)""")
parser.add_argument('infile', default='-', help='the path to the file containing the SQL query to execute', type=argparse.FileType('r'), nargs='?')
parser.add_argument('-s', '--separator', default=';\n', help='the separator between individual statements')
parser.add_argument('-p', '--progress', default=-1, type=int, help='show progress after this amount of executions when inserting/updating large data sets')

class Item:
    def __init__(self, connection, row):
        self.connection = connection
        self.row = row
    def __str__(self):
        return '\t'.join(map(lambda c: unicode(c), self.row))

def read_sql(file):
    start = time.time()

    try:
        sql = file.read()
    except KeyboardInterrupt:
        sql = None
    finally:
        file.close()

    logduration('Reading input statements', start)
    
    return sql

def read_statements(file):
    sql = read_sql(file)

    if not sql:
        return None

    start = time.time()

    stmts = filter(lambda s: len(s.strip()) > 0, sqlparse.split(sql))

    logduration('Splitting SQL statements', start)
    logger.info('Number of SQL statements: %d', len(stmts))
    
    return stmts

class DatabaseExecuter:
    """The main class"""

    @staticmethod
    def execute(options):
        """The main method that splits the arguments and starts the magic"""

        cons = Source.connections()

        # Search exact match of connection
        for connection in cons:
            opts = options.get(connection.driver)
            if connection.matches(opts) and opts.show in ['databases', 'tables', 'columns', 'values']:
                # Reads the statements
                stmts = read_statements(opts.infile)

                # Exit gracefully when no statements have been found (or the input got cancelled)
                if not stmts:
                    return []

                # Collects results
                results = []
                # Counts the changes (inserts, updates)
                changes = 0
                # Counts the statements
                counter = 0
                    
                start = None
                trans = None
                try:
                    # Connects to the database and starts a transaction
                    connection.connect(opts.database)
                    trans = connection.begin()

                    start = time.time()
                    for stmt in stmts:
                        result = connection.execute(stmt, '%d' % counter)
                        if result.cursor:
                            results.extend(map(lambda row: Item(connection, row), result))
                        else:
                            # increase changes based on the returned result info
                            changes += result.rowcount
                        if opts.progress > 0 and counter % opts.progress == 0:
                            sys.stdout.write('.')
                            sys.stdout.flush()
                        counter += 1
                    if opts.progress > 0 and counter >= opts.progress:
                        sys.stdout.write('\n')
                    trans.commit()
                except:
                    if trans:
                        trans.rollback()
                    raise
                finally:
                    connection.close()
                    if start:
                        logduration('Executing SQL statements', start)

                if not results:
                    print 'Changed rows: {0}'.format(changes)
                return results

        raise Exception('Specify the complete URI to a table')

def main():
    wrapper(run)

def default_formatter():
    Writer.set()
def insert_formatter():
    Writer.set(SqlInsertWriter())
def test_formatter():
    Writer.set(StdoutWriter(u'{0}', u'{item}'))

def run(argv):
    options = Config.init(argv, parser)

    if options.formatter:
        Writer.set(options.formatter())
    else:
        Writer.set(ExecuteWriter())

    try:
        return DatabaseExecuter.execute(options)
    except BaseException, e:
        logger.exception(e)
        raise

if __name__ == "__main__":
    main()
