# -*- coding: utf-8 -*-
#
# Copyright © 2014 René Samselnig
#
# This file is part of Database Navigator.
#
# Database Navigator is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Database Navigator is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Database Navigator.  If not, see <http://www.gnu.org/licenses/>.
#

import time
import sys
import sqlparse
import re

from dbnav import Wrapper
from dbnav.config import Config
from dbnav.writer import Writer
from dbnav.sources import Source
from dbnav.logger import logger, logduration, log_error

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


class BaseExecuter:
    def begin(self):
        pass

    def commit(self):
        pass

    def rollback(self):
        pass

    def execute(self, stmt):
        pass

    def write(self, items):
        sys.stdout.write(Writer.write(items))
        sys.stdout.write('\n')


class DefaultExecuter(BaseExecuter):
    """Execute in wrapped transaction"""

    def __init__(self, connection, opts):
        self.connection = connection
        self.opts = opts
        self.trans = None

    def begin(self):
        self.trans = self.connection.begin()

    def commit(self):
        if self.trans:
            self.trans.commit()

    def rollback(self):
        if self.trans:
            self.trans.rollback()

    def execute(self, stmt):
        changes = 0
        results = []

        result = self.connection.execute(stmt)
        if result.cursor:
            items = map(lambda row: Item(self.connection, row), result)
            results.extend(items)
            self.write(items)
        else:
            # increase changes based on the returned result
            # info
            changes += result.rowcount

        return (results, changes, 0)


class IsolationExecuter(BaseExecuter):
    """Execute in wrapped transaction"""

    def __init__(self, connection, opts):
        self.connection = connection
        self.opts = opts

    def execute(self, stmt):
        results = []
        changes = 0
        errors = 0

        try:
            # If we're about to ignore errors we need to
            # use a separate transaction for each
            # statement - otherwise previously successful
            # executions would get lost
            trans = self.connection.begin()

            result = self.connection.execute(stmt)
            if result.cursor:
                items = map(lambda row: Item(self.connection, row), result)
                results.extend(items)
                self.write(items)
            else:
                # increase changes based on the returned result
                # info
                changes = result.rowcount

            if self.opts.dry_run:
                trans.rollback()
            else:
                trans.commit()
        except BaseException as e:
            trans.rollback()
            if not self.opts.mute_errors:
                log_error(e)
            errors += 1

        return (results, changes, errors)


class DatabaseExecuter(Wrapper):
    """The main class"""
    def __init__(self, options):
        self.options = options

        if options.formatter:
            Writer.set(options.formatter(options))
        else:
            Writer.set(ExecuteWriter())

    def write(self):
        try:
            self.run()
        except:
            return -1
        return 0

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
                # Counts the errors (useful with option --ignore-errors)
                errors = 0
                # Counts the statements
                counter = 0

                start = None
                executer = None
                try:
                    # Connects to the database and starts a transaction
                    connection.connect(opts.database)

                    start = time.time()
                    if opts.isolate_statements:
                        executer = IsolationExecuter(connection, opts)
                    else:
                        executer = DefaultExecuter(connection, opts)

                    executer.begin()

                    for stmt in stmts:
                        res, changed, failed = executer.execute(stmt)
                        results.extend(res)
                        changes += changed
                        errors += failed
                        counter += 1

                        if (opts.progress > 0
                                and counter % opts.progress == 0):
                            sys.stdout.write('.')
                            sys.stdout.flush()

                    if opts.dry_run:
                        executer.rollback()
                    else:
                        executer.commit()

                    if opts.progress > 0 and counter >= opts.progress:
                        sys.stdout.write('\n')
                except:
                    errors += 1
                    if executer:
                        executer.rollback()
                    if not opts.mute_errors:
                        raise
                finally:
                    connection.close()
                    if start:
                        logduration('Executing SQL statements', start)

                if not results:
                    dry_run = ''
                    if opts.dry_run:
                        dry_run = ' (dry run)'
                    sys.stdout.write(
                        'Changed rows: {0}{1}\n'.format(changes, dry_run))
                if errors:
                    sys.stdout.write('Errors: {0}'.format(errors))

                return results

        raise Exception('Specify the complete URI to a database')


def run(args):
    executer = DatabaseExecuter(Config.init(args, parser))
    return executer.run()


def main(args=None):
    if args is None:
        args = sys.argv[1:]
    executer = DatabaseExecuter(Config.init(args, parser))
    return executer.write()
