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

from difflib import get_close_matches

from dbmanagr.logger import logger

CONNECTION_NOT_FOUND = 'Connection "{0}" was not found ({1})'
TABLE_NOT_FOUND = 'Table "{0}" was not found ({1})'
COLUMN_NOT_FOUND = 'Column "{0}" was not found on table "{1}" ({2})'
CLOSE_MATCHES = 'close matches: {0}'
NO_CLOSE_MATCHES = 'no close matches in: {0}'


def unknown_connection_message(connection, haystack):
    matches = get_close_matches(connection, haystack)
    if not matches:
        return CONNECTION_NOT_FOUND.format(connection, 'no close matches')
    return CONNECTION_NOT_FOUND.format(
        connection,
        CLOSE_MATCHES.format(u', '.join(matches)))


def unknown_table_message(tablename, haystack):
    if tablename is None:
        tablename = '?'
    matches = get_close_matches(tablename, haystack)
    if not matches:
        return TABLE_NOT_FOUND.format(
            tablename,
            NO_CLOSE_MATCHES.format(u', '.join(haystack)))
    return TABLE_NOT_FOUND.format(
        tablename,
        CLOSE_MATCHES.format(u', '.join(matches)))


def unknown_column_message(table, column, haystack=None):
    if haystack is None:
        haystack = map(lambda c: c.name, table.columns())
    logger.debug('haystack: %s', haystack)
    matches = get_close_matches(column, haystack)
    if not matches:
        return COLUMN_NOT_FOUND.format(
            column,
            table.name if table else '?',
            NO_CLOSE_MATCHES.format(u', '.join(haystack)))
    return COLUMN_NOT_FOUND.format(
        column,
        table.name if table else '?',
        CLOSE_MATCHES.format(u', '.join(matches)))


class BusinessException(Exception):
    pass


class UnknownConnectionException(BusinessException):
    def __init__(self, connection, haystack):
        super(UnknownConnectionException, self).__init__(
            unknown_connection_message(connection, haystack))


class UnknownTableException(BusinessException):
    def __init__(self, tablename, haystack):
        super(UnknownTableException, self).__init__(
            unknown_table_message(tablename, haystack))


class UnknownColumnException(BusinessException):
    def __init__(self, table, column, haystack=None):
        super(UnknownColumnException, self).__init__(
            unknown_column_message(table, column, haystack))
