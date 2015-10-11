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

import logging
import math
import datetime

from urlparse import urlparse
from sqlalchemy import Boolean, Float, Integer
from decimal import Decimal

from dbmanagr.logger import LogWith
from dbmanagr.queryfilter import QueryFilter, OrOp, AndOp
from dbmanagr.utils import escape_statement

OR_OPERATOR = '|'
AND_OPERATOR = '&'
OPERATORS = ['>=', '<=', '!=', '=', '~', '*', '>', '<', ':']

OPTION_URI_FORMAT = '%s@%s/%s'

logger = logging.getLogger(__name__)


def escape_keyword(keyword):
    if keyword in ['user', 'table', 'column']:
        return '"%s"' % keyword
    return keyword


@LogWith(logger)
def restriction(alias, column, operator, value, map_null_operator=True):
    if not column:
        raise Exception('Parameter column may not be None!')
    if operator in ['=', '!='] and (value is None or value == 'null'):
        if map_null_operator:
            operator = {
                '=': 'is',
                '!=': 'is not'
            }.get(operator)
        value = None
    if column.tablename and alias is not None:
        return u"{0}.{1} {2} {3}".format(
            alias,
            escape_keyword(column.name),
            operator,
            format_value(column, value))
    return u'{0} {1} {2}'.format(
        escape_keyword(column.name),
        operator,
        format_value(column, value))


def format_value(column, value):
    if value is None or (type(value) is float and math.isnan(value)):
        return 'null'
    if type(value) is list:
        return '({0})'.format(
            ', '.join([format_value(column, v) for v in value]))
    if type(value) in [datetime.datetime, datetime.date, datetime.time]:
        return "'%s'" % value
    if type(value) is buffer:
        return u"'[BLOB]'"
    if column is None:
        try:
            return '%d' % int(value)
        except ValueError:
            return u"'%s'" % value
    if (isinstance(column.type, Boolean)
            and (type(value) is bool or value in ['true', 'false'])
            or type(value) is bool):
        return '%s' % str(value).lower()
    if isinstance(column.type, Float) or type(value) is float:
        try:
            return '%f' % float(value)
        except ValueError:
            pass
    if isinstance(column.type, Integer) or type(value) in (int, Decimal):
        try:
            return '%d' % int(value)
        except ValueError:
            pass
    return u"'%s'" % escape_statement(value).replace("'", "''")


def parse_filter(s):
    _or = OrOp()
    for t in s.split(OR_OPERATOR):
        _and = AndOp()
        for term in t.split(AND_OPERATOR):
            found = False
            for operator in OPERATORS:
                if operator in term:
                    f = term.split(operator, 1)
                    lhs = f[0]
                    rhs = f[1] if len(f) > 1 else None
                    if operator == ':':
                        rhs = rhs.split(',')
                    _and.append(QueryFilter(lhs, operator, rhs))
                    found = True
                    break
            if not found:
                _and.append(QueryFilter(term))
        _or.append(_and)
    return _or


class Options(object):
    parser = {}

    def __init__(self, argv, parser):
        logger.info('Called with params: %s', argv)

        self.opts = {}
        self.argv = argv
        self.uri = None
        self.logfile = None
        self.loglevel = None
        self.database = None
        self.table = None
        self.column = ''
        self.operator = None
        self.filter = None
        self.show = 'connections'
        self.simplify = False
        self.prog = parser.prog
        self.daemon = False
        self.command = None
        self.left = None
        self.right = None

        args = parser.parse_args(argv)

        if hasattr(args, 'include'):
            args.include = args.include.split(',') if args.include else []
        if hasattr(args, 'exclude'):
            args.exclude = args.exclude.split(',') if args.exclude else []

        self.__dict__.update(args.__dict__)

        self.update_parsers()

    def update_parsers(self):
        for k in Options.parser:
            self.opts[k] = Options.parser[k].parse(self)

    def get(self, parser):
        return self.opts[parser]

    def escape_keyword(self, keyword):
        return escape_keyword(keyword)

    def restriction(
            self, alias, column, operator, value, map_null_operator=True):
        return restriction(alias, column, operator, value, map_null_operator)

    def format_value(self, column, value):
        return format_value(column, value)

    def __setattr__(self, name, value):
        self.__dict__[name] = value
        if self.opts:
            for k in self.opts.keys():
                self.opts[k].__dict__[name] = value

    def __repr__(self):
        return self.__dict__.__repr__()


class OptionsParser(object):
    def create_driver(self):  # pragma: no cover
        pass

    def parse(self, source):  # pragma: no cover
        pass


class FileOptionsParser(OptionsParser):
    def parse(self, source):
        driver = self.create_driver()
        driver.__dict__.update(source.__dict__)
        if driver.uri:
            uri = driver.uri
            url = urlparse('url://%s' % uri)
            paths = url.path.split('?')[0].split('/')

            if len(paths) > 1:
                driver.table = paths[1]
            if '?' in uri:
                driver.filter = parse_filter(url.query)
                paths.append(url.query)

            driver.show_code = len(paths)
            driver.show = {
                1: 'connections',
                2: 'tables',
                3: 'columns',
                4: 'values'
            }.get(driver.show_code, 'connections')

        return driver


class UriOptionsParser(OptionsParser):
    def parse(self, source):
        driver = self.create_driver()
        driver.__dict__.update(source.__dict__)
        if driver.uri:
            uri = driver.uri
            if '@' not in uri:
                uri += '@'
            url = urlparse('url://%s' % uri)
            locs = url.netloc.split('@')
            paths = url.path.split('?')[0].split('/')

            if len(locs) > 0:
                driver.user = locs[0]
            if len(locs) > 1 and '@' in driver.uri:
                driver.host = locs[1]
            if len(paths) > 1:
                driver.database = paths[1]
            if len(paths) > 2:
                driver.table = paths[2]
            if '?' in uri:
                driver.filter = parse_filter(url.query)
                paths.append(url.query)

            driver.show_code = len(paths)
            driver.show = {
                1: 'connections',
                2: 'databases',
                3: 'tables',
                4: 'columns',
                5: 'values'
            }.get(driver.show_code, 'connections')

        if driver.user and driver.host:
            driver.gen = OPTION_URI_FORMAT % (
                driver.user,
                driver.host,
                driver.table if driver.table else ''
            )

        return driver
