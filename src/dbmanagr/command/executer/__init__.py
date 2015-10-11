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

import sys
import sqlparse
import re

from datetime import datetime

from dbmanagr.wrapper import Wrapper
from dbmanagr.config import Config
from dbmanagr.writer import Writer
from dbmanagr.utils import find_connection
from dbmanagr.sources.source import Source
from dbmanagr.logger import logger, LogTimer, log_error
from dbmanagr.exception import UnknownConnectionException
from dbmanagr.dto.mapper import to_dto

from .args import parser
from .writer import ExecuteWriter

EXECUTION_START = {
    1: '{statement}\n',
    2: '{time:%H:%M:%S.%f}: executing: {statement}\n',
    3: '{time:%Y-%m-%d %H:%M:%S.%f}: executing: {statement}\n'
}
EXECUTION_END = {
    2: '{time:%H:%M:%S.%f}: execution took: {duration}s\n',
    3: '{time:%Y-%m-%d %H:%M:%S.%f}: execution took: {duration}s\n'
}


class Item(object):
    def __init__(self, connection, row):
        self.connection = connection
        self.row = row

    def __str__(self):
        return '\t'.join(map(unicode, self.row))


def read_sqls(files):
    sql = ''

    for file_ in files:
        sql += read_sql(file_)

    return sql


def read_sql(file_):
    timer = LogTimer(logger, 'Reading input statements')

    try:
        sql = file_.read()
    except KeyboardInterrupt:  # pragma: no cover
        sql = None
    finally:
        file_.close()

    timer.stop()

    return sql


def read_statements(opts):
    if opts.statements is not None:
        sql = opts.statements
    else:
        sql = read_sqls(opts.infile)

    if not sql:
        return None

    timer = LogTimer(logger, 'Splitting SQL statements')

    # Removes the shebang, if any
    sql = re.sub(r'^#!.*\n', '', sql)

    stmts = filter(lambda s: len(s.strip()) > 0, sqlparse.split(sql))

    timer.stop()

    logger.info('Number of SQL statements: %d', len(stmts))

    return stmts


def trim_space(stmt):
    return re.sub(r'\s+', ' ', unicode(stmt))


class BaseExecuter(object):
    def begin(self):  # pragma: no cover
        pass

    def commit(self):  # pragma: no cover
        pass

    def rollback(self):  # pragma: no cover
        pass

    def execute(self, stmt):  # pragma: no cover
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
            results = map(lambda row: Item(self.connection, row), result)
            self.write(results)
        else:
            # increase changes based on the returned result info
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
                results = map(lambda row: Item(self.connection, row), result)
                self.write(results)
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
        Wrapper.__init__(self, options)

        if options.formatter:
            Writer.set(options.formatter(options))
        else:
            Writer.set(ExecuteWriter())

    def write(self):
        try:
            self.run()
        except BaseException:
            return -1
        return 0

    def execute(self):
        """The main method that splits the arguments and starts the magic"""
        options = self.options

        # search exact match of connection
        connection, opts = find_connection(
            Source.connections(),
            options,
            lambda con, opts: (
                con.matches(opts)
                and opts.show in ['databases', 'tables', 'columns', 'values']))

        if connection is None:
            raise UnknownConnectionException(
                options.uri,
                map(lambda c: c.autocomplete(), Source.connections()))

        return self.process(connection, opts)

    def process(self, connection, opts):
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

        timer = None
        executer = None
        try:
            # Connects to the database and starts a transaction
            connection.connect(opts.database)

            timer = LogTimer(logger, 'Executing SQL statements')

            if opts.isolate_statements:
                executer = IsolationExecuter(connection, opts)
            else:
                executer = DefaultExecuter(connection, opts)

            executer.begin()

            for stmt in stmts:
                start = datetime.now()
                sys.stdout.write(
                    EXECUTION_START.get(opts.verbose, '').format(
                        time=start,
                        statement=stmt))

                res, changed, failed = executer.execute(stmt)
                results.extend(res)
                changes += changed
                errors += failed
                counter += 1

                if opts.progress > 0 and counter % opts.progress == 0:
                    sys.stderr.write('.')
                    sys.stderr.flush()

                end = datetime.now()
                sys.stdout.write(
                    EXECUTION_END.get(opts.verbose, '').format(
                        time=end,
                        statement=trim_space(stmt),
                        duration=(end - start).total_seconds()))

            if opts.dry_run:
                executer.rollback()
            else:
                executer.commit()

            if opts.progress > 0 and counter >= opts.progress:
                # Write a new line after progress indicator dots have
                # been written
                sys.stderr.write('\n')
        except BaseException:
            errors += 1
            if executer:
                executer.rollback()
            if not opts.mute_errors:
                raise
        finally:
            connection.close()
            if timer:
                timer.stop()

        if not results:
            dry_run = ''
            if opts.dry_run:
                dry_run = ' (dry run)'
            sys.stdout.write(
                'Changed rows: {0}{1}\n'.format(changes, dry_run))
        if errors:
            sys.stdout.write('Errors: {0}'.format(errors))

        return to_dto(results)


def execute(args):
    """
    Directly calls the execute method and avoids using the wrapper
    """
    return DatabaseExecuter(Config.init(args, parser)).execute()


def run(args):
    return DatabaseExecuter(Config.init(args, parser)).run()


def main(args=None):
    if args is None:
        args = sys.argv[1:]
    return DatabaseExecuter(Config.init(args, parser)).write()
