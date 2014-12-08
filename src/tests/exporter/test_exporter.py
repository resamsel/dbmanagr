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

from tests.exporter import load
from tests.testcase import DbTestCase
from tests.mock.sources import MockSource
from dbnav import exporter
from dbnav.exception import UnknownTableException, UnknownColumnException


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

        self.assertEqual(
            '!!null null',
            exporter.writer.yaml_value(user.column('id'), None))
        self.assertEqual(
            '!!float 3.141500',
            exporter.writer.yaml_value(user.column('score'), 3.141500))
        self.assertEqual(
            '!!bool true',
            exporter.writer.yaml_value(user.column('deleted'), True))

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
            exporter.main)
        self.assertEqual(
            0,
            exporter.main(['dbnav.sqlite/user?id=1']))
