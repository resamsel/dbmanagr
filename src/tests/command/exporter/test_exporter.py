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

from decimal import Decimal
from sqlalchemy.util import KeyedTuple

from tests.command.exporter import load
from tests.testcase import DbTestCase
from tests.mock.sources import MockSource
from dbnav.command import exporter
from dbnav.exception import UnknownTableException, UnknownColumnException, \
    UnknownConnectionException
from dbnav.utils import mute_stderr
from dbnav.dto.mapper import to_dto
from dbnav.model.row import Row


def test_exporter():
    os.environ['UNITTEST'] = 'True'
    for test in load():
        yield test,
    del os.environ['UNITTEST']


class DifferTestCase(DbTestCase):
    def test_yaml_value(self):
        """Tests the exporter.writer.yaml_value function"""

        DbTestCase.connection.close()
        DbTestCase.connection = MockSource().list()[0]
        DbTestCase.connection.connect()
        con = DbTestCase.connection
        user = con.table('user2')
        user_dto = to_dto(user)

        self.assertEqual(
            u'!!null null',
            exporter.writer.yaml_value(
                to_dto(user.column('id')), user_dto, None))
        self.assertEqual(
            u'!!float 3.141500',
            exporter.writer.yaml_value(
                to_dto(user.column('score')), user_dto, 3.141500))
        self.assertEqual(
            u'Yes',
            exporter.writer.yaml_value(
                to_dto(user.column('deleted')), user_dto, True))
        self.assertEqual(
            u'!!str Yes',
            exporter.writer.yaml_value(
                to_dto(user.column('url')), user_dto, 'Yes'))
        self.assertEqual(
            u'!!int 3',
            exporter.writer.yaml_value(
                to_dto(user.column('score')), user_dto, Decimal(3.0)))
        self.assertEqual(
            u'!!float 3.100000',
            exporter.writer.yaml_value(
                to_dto(user.column('score')), user_dto, Decimal(3.1)))

    def test_unknown_connection(self):
        """Tests unknown connection"""

        self.assertRaises(
            UnknownConnectionException,
            exporter.run,
            ['unknown'])

    def test_unknown_table(self):
        """Tests unknown tables"""

        self.assertRaises(
            Exception,
            exporter.run,
            ['dbnav.sqlite'])
        self.assertRaises(
            UnknownTableException,
            exporter.run,
            ['dbnav.sqlite/unknown?'])

    def test_unknown_column(self):
        """Tests unknown columns"""

        self.assertRaises(
            UnknownColumnException,
            exporter.run,
            ['dbnav.sqlite/user2?', '-i', 'unknown'])
        self.assertRaises(
            UnknownColumnException,
            exporter.run,
            ['dbnav.sqlite/user2?', '-x', 'unknown'])

    def test_foreign_keys(self):
        """Tests foreign keys"""

        pass

    def test_writer(self):
        """Tests the writer"""

        import sys
        sys.argv = ['']

        self.assertRaises(
            SystemExit,
            mute_stderr(exporter.main))

        self.assertEqual(
            0,
            exporter.main(['dbnav.sqlite/user?id=1']))

    def test_execute(self):
        """Tests the exporter.execute function"""

        self.assertRaises(
            SystemExit,
            mute_stderr(exporter.execute),
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

        item = exporter.RowItem(row, None, None, None)

        self.assertEqual(item, item)

        self.assertEqual(
            item,
            exporter.RowItem.from_json({
                'row': row,
                'include': None,
                'exclude': None,
                'substitutes': None
            })
        )
