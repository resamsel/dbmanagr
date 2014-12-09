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

from tests.grapher import load
from tests.testcase import DbTestCase
from dbnav import grapher
from dbnav.config import Config
from dbnav.exception import UnknownTableException


def test_grapher():
    os.environ['UNITTEST'] = 'True'
    for test in load():
        yield test,
    del os.environ['UNITTEST']


class GrapherTestCase(DbTestCase):
    def test_unknown_table(self):
        """Tests unknown tables"""

        self.assertRaises(
            Exception,
            grapher.run,
            ['dbnav.sqlite'])
        self.assertRaises(
            UnknownTableException,
            grapher.run,
            ['dbnav.sqlite/unknown?'])

    def test_writer(self):
        """Tests the writer"""

        import sys
        sys.argv = ['']

        self.assertRaises(
            SystemExit,
            self.mute_stderr(grapher.main))

        self.assertEqual(
            0,
            grapher.main(['dbnav.sqlite/user?id=1']))

    def test_options(self):
        """Tests options"""

        config = Config.init(
            ['-r', '--database', 'dbnav.sqlite/article'],
            grapher.args.parser)
        config.database = 'db'

        self.assertEqual(
            12,
            len(grapher.DatabaseGrapher(config).run()))
