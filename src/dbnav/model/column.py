#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
from .baseitem import BaseItem

logger = logging.getLogger(__name__)

class Column(BaseItem):
    """A table column"""

    def __init__(self, table, name, primary_key=False, type=None):
        self.table = table
        self.name = name
        self.primary_key = primary_key
        self.type = type

        #logger.debug('Column: %s', self.__dict__)

    def __repr__(self):
        return '%s.%s' % (self.table.name, self.name)

    def title(self):
        return self.name

    def subtitle(self):
        return self.table.title()

    def autocomplete(self):
        return '%s%s/%s' % (self.table.uri, self.table.name, self.name)

    def icon(self):
        return 'images/table.png'
