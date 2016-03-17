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

from datetime import datetime
from humanize import naturaltime

from dbmanagr.writer import TabularWriter


def format_date(d):
    if d is None:
        return ''
    return naturaltime(datetime.now().replace(tzinfo=d.tzinfo) - d)
    # return u'{:%Y-%m-%d %H:%M:%S}'.format(d)


def format_delta(d):
    if d is None:
        return ''
    # return naturaldelta(d)
    return str(d)


DEFAULT_FORMAT = u'{0}'
HEADERS = {
    -1: [],  # for testing only
    0: [],
    1: [
        u'PID', u'Database', u'User', u'Client', u'Query Start', u'State',
        u'Blocked by', u'Query'
    ],
    2: [
        u'PID', u'Database', u'User', u'Application', u'Client', u'TX Start',
        u'TX Duration', u'Query Start', u'Query Duration', u'State',
        u'Blocked by', u'Query'
    ],
}
VALUES = {
    0: lambda row: [row.pid, row.state, row.query_duration, row.query],
    1: lambda row: [
        row.pid, row.database_name, row.username, row.client,
        format_date(row.query_start), row.state, row.blocked_by, row.query
    ],
    2: lambda row: [
        row.pid, row.database_name, row.username, row.application, row.client,
        format_date(row.transaction_start),
        format_delta(row.transaction_duration),
        format_date(row.query_start), format_delta(row.query_duration),
        row.state, row.blocked_by, row.query
    ],
}


class StatementActivityWriter(TabularWriter):
    def __init__(self, options):
        super(StatementActivityWriter, self).__init__(
            options,
            lambda items: HEADERS.get(options.verbose, HEADERS[0]),
            VALUES.get(options.verbose, VALUES[0])
        )
