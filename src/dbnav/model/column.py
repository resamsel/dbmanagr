#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging

logger = logging.getLogger(__name__)

class Column:
    """A table column"""

    def __init__(self, table, name, primary_key=False):
        self.table = table
        self.name = name
        self.primary_key = primary_key

        #logger.debug('Column: %s', self.__dict__)

    def __repr__(self):
        return '%s.%s' % (self.table.name, self.name)

    def autocomplete(self):
        return '%s%s/%s' % (self.table.uri, self.table.name, self.name)