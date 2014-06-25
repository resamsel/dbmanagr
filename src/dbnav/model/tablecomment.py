#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json

COMMENT_ID = 'id'
COMMENT_TITLE = 'title'
COMMENT_SUBTITLE = 'subtitle'
COMMENT_ORDER_BY = 'order'
COMMENT_SEARCH = 'search'
COMMENT_DISPLAY = 'display'

class TableComment:
    """The comment on the given table that allows to display much more accurate information"""

    def __init__(self, table, json_string):
        self.d = {COMMENT_ORDER_BY: [], COMMENT_SEARCH: [], COMMENT_DISPLAY: []}
        self.id = None
        self.title = None
        self.subtitle = None

        if json_string:
            try:
                self.d = dict(self.d.items() + json.loads(json_string).items())
            except TypeError, e:
                pass

        if COMMENT_ID in self.d:
            self.id = self.d[COMMENT_ID]
        if COMMENT_TITLE in self.d and self.id:
            self.d[COMMENT_TITLE] = '{0}.%s' % self.id
        if COMMENT_TITLE in self.d:
            self.title = self.d[COMMENT_TITLE]
        if COMMENT_SUBTITLE in self.d:
            self.subtitle = self.d[COMMENT_SUBTITLE]
        self.search = self.d[COMMENT_SEARCH]
        self.display = self.d[COMMENT_DISPLAY]
        self.order = self.d[COMMENT_ORDER_BY]

    def __repr__(self):
        return self.d.__repr__()

