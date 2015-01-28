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

from dbnav.writer import FormatWriter
from dbnav.formatter import Formatter, DefaultFormatter

DEFAULT_FORMAT = u'{0}'
VERBOSE_FORMAT = u'PID\tDatabase\tUser\tClient\tQuery Start\tBlocked by\t'\
    u'Query\n{0}'


class StatementActivityWriter(FormatWriter):
    def __init__(self, options):
        FormatWriter.__init__(
            self,
            VERBOSE_FORMAT if options.verbose > 0 else DEFAULT_FORMAT,
            u'{row.pid}\t{row.database_name}\t{row.username}\t{row.client}\t'
            u'{row.query_start}\t{row.state}\t{row.blocked_by}\t{row.query}')
        Formatter.set(DefaultFormatter())
        self.options = options

    def itemtostring(self, item):
        row = item.row
        return self.item_format.format(row=row)
