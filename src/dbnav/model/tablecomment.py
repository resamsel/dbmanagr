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
import json

COMMENT_ID = 'id'
COMMENT_TITLE = 'title'
COMMENT_SUBTITLE = 'subtitle'
COMMENT_ORDER_BY = 'order'
COMMENT_SEARCH = 'search'
COMMENT_DISPLAY = 'display'

logger = logging.getLogger(__name__)


class TableComment(object):
    """The comment on the given table that allows to display much more
accurate information"""

    def __init__(self, json_string):
        self.id = None
        self.title = None
        self.subtitle = None
        self.search = None
        self.display = None
        self.order = None

        self.parse(json_string)

    def parse(self, json_string):
        d = {
            COMMENT_ORDER_BY: [],
            COMMENT_SEARCH: [],
            COMMENT_DISPLAY: []
        }

        if json_string:
            try:
                d.update(json.loads(json_string))
            except BaseException as e:
                logger.warn('Error parsing JSON comment: %s', e)

        if COMMENT_ID in d:
            self.id = d[COMMENT_ID]
        if COMMENT_TITLE in d and self.id:
            d[COMMENT_TITLE] = u'{0}.%s' % self.id
        if COMMENT_TITLE in d:
            self.title = d[COMMENT_TITLE]
        if COMMENT_SUBTITLE in d:
            self.subtitle = d[COMMENT_SUBTITLE]
        self.search = d[COMMENT_SEARCH]
        self.display = d[COMMENT_DISPLAY]
        self.order = d[COMMENT_ORDER_BY]

    def __repr__(self):
        return self.__dict__.__repr__()
