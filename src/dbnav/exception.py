#!/usr/bin/env python
# -*- coding: utf-8 -*-

from difflib import get_close_matches

from dbnav.logger import logger

CLOSE_MATCHES = 'Column "{0}" was not found on table "{1}" '\
    '(close matches: {2})'
NO_CLOSE_MATCHES = 'Column "{0}" was not found on table "{1}" '\
    '(no close matches in {2})'


def unknown_column_message(table, column, haystack=None):
    if haystack is None:
        haystack = map(lambda c: c.name, table.columns())
    logger.debug('haystack: %s', haystack)
    matches = get_close_matches(column, haystack)
    if not matches:
        return NO_CLOSE_MATCHES.format(
            column,
            table.name if table else '?',
            haystack)
    return CLOSE_MATCHES.format(
        column,
        table.name if table else '?',
        u', '.join(matches))


class UnknownColumnException(Exception):
    def __init__(self, table, column, haystack=None):
        super(UnknownColumnException, self).__init__(
            unknown_column_message(table, column, haystack))
