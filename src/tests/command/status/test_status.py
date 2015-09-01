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

import os

from sqlalchemy.util import KeyedTuple

from tests.command.status import load
from tests.testcase import DbTestCase
from dbnav.command import status
from dbnav.utils import mute_stderr
from dbnav.model.row import Row


def test_argumentor():
    os.environ['UNITTEST'] = 'True'
    for test in load():
        yield test,
    del os.environ['UNITTEST']


class Options(object):
    def __init__(self):
        self.verbose = -1


class StatusTestCase(DbTestCase):
    def test_writer(self):
        """Tests the writer"""

        import sys
        sys.argv = ['']

        self.assertRaises(
            SystemExit,
            mute_stderr(status.main)
        )
        self.assertRaises(
            SystemExit,
            mute_stderr(status.main),
            []
        )
        self.assertRaises(
            Exception,
            mute_stderr(status.execute),
            ['unknown']
        )

    def test_execute(self):
        """Tests the status.execute function"""

        self.assertRaises(
            SystemExit,
            mute_stderr(status.execute),
            []
        )

    def test_row_item(self):
        """Tests the RowItem class"""

        row = Row(None, KeyedTuple(
            [
                '', -1, '', '', None, None, '',
                '', '', '', -1, -1],
            labels=[
                'database_name', 'pid', 'username', 'client',
                'transaction_start', 'query_start', 'state', 'query',
                'blocked', 'blocked_by', 'transaction_duration',
                'query_duration']
        ))

        item = status.RowItem(row)

        self.assertEqual(item, item)

        self.assertEqual(
            item,
            status.RowItem.from_json({'row': row})
        )
        self.assertIsNotNone(
            status.writer.StatementActivityWriter(Options()).itemtostring(
                item
            )
        )
