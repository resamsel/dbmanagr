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

from dbmanagr.model.baseitem import BaseItem
from dbmanagr.formatter import Formatter
from dbmanagr.utils import primary_key_or_first_column

logger = logging.getLogger(__name__)


def val(row, column):
    # colname = '%s_title' % column
    # if colname in row.row:
    #     return '%s (%s)' % (row.row[colname], row.row[column])
    return row[column]


class Row(BaseItem):
    """A table row from the database"""

    def __init__(self, table, row):
        self.table = table
        self.row = row

    def __getitem__(self, i):
        if i is None:
            return None
        if type(i) == unicode:
            i = i.encode('ascii')
        if type(i) is str:
            try:
                return self.row.__dict__[i]
            except BaseException:
                return None
        return self.row[i]

    def __repr__(self):
        return str(self.row)

    def title(self):
        if 'title' in self.row.__dict__:
            return val(self, 'title')
        return val(self, primary_key_or_first_column(self.table))

    def subtitle(self):
        return val(self, 'subtitle')

    def autocomplete(self):
        column = primary_key_or_first_column(self.table)
        return self.table.autocomplete_(column, self[column])

    def icon(self):
        return 'images/row.png'

    def format(self):
        return Formatter.format_row(self)
