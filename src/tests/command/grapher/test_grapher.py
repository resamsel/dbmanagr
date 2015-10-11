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

from tests.command.grapher import load
from tests.testcase import DbTestCase
from dbmanagr.command import grapher
from dbmanagr.config import Config
from dbmanagr.exception import UnknownTableException, \
    UnknownConnectionException
from dbmanagr.utils import mute_stderr


def test_grapher():
    os.environ['UNITTEST'] = 'True'
    for test in load():
        yield test,
    del os.environ['UNITTEST']


class GrapherTestCase(DbTestCase):
    def test_unknown_connection(self):
        """Tests unknown connection"""

        self.assertRaises(
            UnknownConnectionException,
            grapher.run,
            ['unknown'])

    def test_unknown_table(self):
        """Tests unknown tables"""

        self.assertRaises(
            Exception,
            grapher.run,
            ['dbmanagr.sqlite'])
        self.assertRaises(
            UnknownTableException,
            grapher.run,
            ['dbmanagr.sqlite/unknown?'])

    def test_writer(self):
        """Tests the writer"""

        import sys
        sys.argv = ['']

        self.assertRaises(
            SystemExit,
            mute_stderr(grapher.main))

        self.assertEqual(
            0,
            grapher.main(['dbmanagr.sqlite/user?id=1']))

    def test_execute(self):
        """Tests the grapher.execute function"""

        self.assertRaises(
            SystemExit,
            mute_stderr(grapher.execute),
            []
        )

    def test_options(self):
        """Tests options"""

        config = Config.init(
            ['-r', '--database', 'dbmanagr.sqlite/article'],
            grapher.args.parser)
        config.database = 'db'

        self.assertEqual(
            12,
            len(grapher.DatabaseGrapher(config).run()))
