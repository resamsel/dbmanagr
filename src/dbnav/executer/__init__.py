#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import sys
import sqlparse
import re

from dbnav import Wrapper
from dbnav.config import Config
from dbnav.writer import Writer
from dbnav.sources import Source
from dbnav.logger import logger, logduration

from .args import parser
from .writer import ExecuteWriter


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


def read_statements(opts):
    if opts.statements:
        sql = opts.statements
    else:
        sql = read_sql(opts.infile)

    if not sql:
        return None

    start = time.time()

    # Removes the shebang, if any
    sql = re.sub(r'^#!.*\n', '', sql)

    stmts = filter(lambda s: len(s.strip()) > 0, sqlparse.split(sql))

    logduration('Splitting SQL statements', start)
    logger.info('Number of SQL statements: %d', len(stmts))

    return stmts


class DatabaseExecuter(Wrapper):
    """The main class"""
    def __init__(self, options):
        self.options = options

        if options.formatter:
            Writer.set(options.formatter(options))
        else:
            Writer.set(ExecuteWriter())

    def execute(self):
        """The main method that splits the arguments and starts the magic"""
        options = self.options

        cons = Source.connections()

        # Search exact match of connection
        for connection in cons:
            opts = options.get(connection.dbms)
            if connection.matches(opts) and opts.show in [
                    'databases', 'tables', 'columns', 'values']:
                # Reads the statements
                stmts = read_statements(opts)

                # Exit gracefully when no statements have been found (or the
                # input got cancelled)
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
                            results.extend(map(
                                lambda row: Item(connection, row), result))
                        else:
                            # increase changes based on the returned result
                            # info
                            changes += result.rowcount
                        if opts.progress > 0 and counter % opts.progress == 0:
                            sys.stdout.write('.')
                            sys.stdout.flush()
                        counter += 1
                    if opts.progress > 0 and counter >= opts.progress:
                        sys.stdout.write('\n')
                    if opts.dry_run:
                        trans.rollback()
                    else:
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
                    dry_run = ''
                    if opts.dry_run:
                        dry_run = ' (dry run)'
                    print 'Changed rows: {0}{1}'.format(changes, dry_run)
                return results

        raise Exception('Specify the complete URI to a database')


def run(args):
    executer = DatabaseExecuter(Config.init(args, parser))
    return executer.run()


def main():
    executer = DatabaseExecuter(Config.init(sys.argv[1:], parser))
    return executer.write()
