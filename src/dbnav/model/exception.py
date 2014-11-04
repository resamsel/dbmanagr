#!/usr/bin/env python
# -*- coding: utf-8 -*-

from difflib import get_close_matches

from dbnav.logger import logger


def unknown_column_message(table, column, haystack=None):
    if haystack is None:
        haystack = map(lambda c: c.name, table.cols)
    logger.debug('haystack: %s', haystack)
    matches = get_close_matches(column, haystack)
    if not matches:
        return 'Column "{0}" was not found on table "{1}" (no close matches in {2})'.format(
            column,
            table.name if table else '?',
            haystack)
    return 'Column "{0}" was not found on table "{1}" (close matches: {2})'.format(
        column,
        table.name if table else '?',
        u', '.join(matches))


class UnknownColumnException(Exception):
    def __init__(self, table, column, haystack=None):
        super(UnknownColumnException, self).__init__(unknown_column_message(table, column, haystack))
