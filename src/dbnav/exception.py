#!/usr/bin/env python
# -*- coding: utf-8 -*-

from difflib import get_close_matches

from dbnav.logger import logger

TABLE_NOT_FOUND = 'Table "{0}" was not found ({1})'
COLUMN_NOT_FOUND = 'Column "{0}" was not found on table "{1}" ({2})'
CLOSE_MATCHES = 'close matches: {0}'
NO_CLOSE_MATCHES = 'no close matches in: {0}'


def unknown_table_message(tablename, haystack):
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


class UnknownTableException(Exception):
    def __init__(self, tablename, haystack):
        super(UnknownTableException, self).__init__(
            unknown_table_message(tablename, haystack))


class UnknownColumnException(Exception):
    def __init__(self, table, column, haystack=None):
        super(UnknownColumnException, self).__init__(
            unknown_column_message(table, column, haystack))
