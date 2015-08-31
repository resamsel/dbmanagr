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

from tests.command.differ import load
from tests.testcase import DbTestCase
from dbnav.command import differ
from dbnav.utils import mute_stderr


def test_differ():
    os.environ['UNITTEST'] = 'True'
    for test in load():
        yield test
    del os.environ['UNITTEST']


class DifferTestCase(DbTestCase):
    def test_unknown_connection(self):
        """Tests unknown connections"""

        self.assertRaises(
            Exception,
            differ.run,
            ['a', 'b'])
        self.assertRaises(
            Exception,
            differ.run,
            ['dbnav.sqlite/user', 'b'])
        self.assertRaises(
            Exception,
            differ.run,
            ['dbnav.sqlite/unknown', 'dbnav-c.sqlite/unknown'])
        self.assertRaises(
            Exception,
            differ.run,
            ['dbnav.sqlite/user', 'dbnav-c.sqlite/unknown'])

    def test_writer(self):
        """Tests the writer"""

        import sys
        sys.argv = ['']

        self.assertRaises(
            SystemExit,
            mute_stderr(differ.main))

        self.assertEqual(
            0,
            differ.main(['dbnav.sqlite/user', 'dbnav.sqlite/user2']))

    def test_execute(self):
        """Tests the differ.execute function"""

        self.assertRaises(
            SystemExit,
            mute_stderr(differ.execute),
            []
        )
