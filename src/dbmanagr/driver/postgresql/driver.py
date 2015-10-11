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

from sqlalchemy import Integer

from dbmanagr.logger import logger, LogWith
from dbmanagr.options import format_value, UriOptionsParser
from dbmanagr.driver import DatabaseDriver

from .version import stat_activity_query


@LogWith(logger)
def restriction(alias, column, operator, value, map_null_operator=True):
    if not column:
        raise Exception('Parameter column may not be None!')
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
            lhs = 'cast({0}{1} as text)'.format(alias, column.name)
    if operator in ['=', '!='] and (value == 'null' or value is None):
        if map_null_operator:
            operator = {
                '=': 'is',
                '!=': 'is not'
            }.get(operator)
        value = None
    rhs = format_value(column, value)

    return ' '.join([lhs, operator, rhs])


class PostgreSQLDriver(DatabaseDriver):
    def __init__(self):
        self.user = None
        self.host = None
        self.gen = None

    @LogWith(logger)
    def restriction(self, *args):
        return restriction(*args)

    def __repr__(self):
        return str(self.__dict__)

    def statement_activity(self, con):
        return con.execute(stat_activity_query(
            con.engine().dialect.server_version_info).format(**self.__dict__))


class PostgreSQLOptionsParser(UriOptionsParser):
    def create_driver(self):
        return PostgreSQLDriver()
