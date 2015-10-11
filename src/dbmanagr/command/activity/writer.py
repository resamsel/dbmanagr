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

from dbmanagr.writer import FormatWriter
from dbmanagr.formatter import Formatter, DefaultFormatter

DEFAULT_FORMAT = u'{0}'
FORMATS = {
    -1: u'{0}\n',  # for testing only
    0: u'{0}\n',
    1: u'PID\tDatabase\tUser\tClient\tTX Start\tQuery Start\tState\t'
       u'Blocked by\tQuery\n{0}\n',
    2: u'PID\tDatabase\tUser\tClient\tTX Start\tTX Duration\tQuery Start\t'
       u'Query Duration\tState\tBlocked by\tQuery\n{0}\n'
}
ITEM_FORMATS = {
    -1: u'{row}',  # for testing only
    0: u'{row.pid}\t{row.state}\t{row.query_duration}\t{row.query}',
    1: u'{row.pid}\t{row.database_name}\t{row.username}\t{row.client}\t'
       u'{row.transaction_start:%Y-%m-%d %H:%M:%S}\t'
       u'{row.query_start:%Y-%m-%d %H:%M:%S}\t{row.state}\t'
       u'{row.blocked_by}\t{row.query}',
    2: u'{row.pid}\t{row.database_name}\t{row.username}\t{row.client}\t'
       u'{row.transaction_start}\t{row.transaction_duration}\t'
       u'{row.query_start}\t{row.query_duration}\t{row.state}\t'
       u'{row.blocked_by}\t{row.query}'
}


class StatementActivityWriter(FormatWriter):
    def __init__(self, options):
        FormatWriter.__init__(
            self,
            FORMATS.get(options.verbose, FORMATS[0]),
            ITEM_FORMATS.get(options.verbose, ITEM_FORMATS[0]))
        Formatter.set(DefaultFormatter())
        self.options = options

    def itemtostring(self, item):
        row = item.row
        return self.item_format.format(row=row)
