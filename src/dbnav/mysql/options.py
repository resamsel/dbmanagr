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

from urlparse import urlparse

from sqlalchemy.types import Integer

from dbnav.logger import LogWith
from dbnav.logger import logger
from dbnav.options import parse_filter, format_value

OPTION_URI_FORMAT = '%s@%s/%s'


@LogWith(logger)
def restriction(
        alias, column, operator, value, map_null_operator=True):
    if operator in ['~', 'like'] and isinstance(column.type, Integer):
        try:
            int(value)
            # LIKE not allowed on integer columns, change operator to
            # equals
            operator = '='
        except ValueError:
            pass

    if alias:
        alias = '{0}.'.format(alias)
    else:
        alias = ''
    lhs = column.name
    if column.table:
        lhs = '{0}{1}'.format(alias, column.name)
    if (value
            and isinstance(column.type, Integer)
            and type(value) is not list):
        try:
            int(value)
        except ValueError:
            # column type is integer, but value is not
            lhs = 'cast({0}{1} as char)'.format(alias, column.name)
    if operator in ['=', '!='] and (value == 'null' or value is None):
        if map_null_operator:
            operator = {
                '=': 'is',
                '!=': 'is not'
            }.get(operator)
        value = None
    rhs = format_value(column, value)

    return ' '.join([lhs, operator, rhs])


class MySQLOptions:
    def __init__(self):
        self.user = None
        self.host = None
        self.gen = None

    def get(self, driver):
        return self

    def restriction(
            self, alias, column, operator, value, map_null_operator=True):
        return restriction(alias, column, operator, value, map_null_operator)

    def __repr__(self):
        return str(self.__dict__)


class MySQLOptionsParser:
    def parse(self, source):
        opts = MySQLOptions()
        opts.__dict__.update(source.__dict__)
        if opts.uri:
            uri = opts.uri
            if '@' not in uri:
                uri += '@'
            url = urlparse('mysql://%s' % uri)
            locs = url.netloc.split('@')
            paths = url.path.split('/')

            if len(locs) > 0:
                opts.user = locs[0]
            if len(locs) > 1 and '@' in opts.uri:
                opts.host = locs[1]
            if len(paths) > 1:
                opts.database = paths[1]
            if len(paths) > 2:
                opts.table = paths[2]
            if '?' in uri:
                opts.filter = parse_filter(url.query)
                paths.append(url.query)

            opts.show = {
                1: 'connections',
                2: 'databases',
                3: 'tables',
                4: 'columns',
                5: 'values'
            }.get(len(paths), 'connections')

        if opts.user and opts.host:
            opts.gen = OPTION_URI_FORMAT % (
                opts.user, opts.host, opts.table if opts.table else ''
            )

        return opts
