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

from sqlalchemy.exc import OperationalError

from tests.executer import load
from tests.testcase import DbTestCase
from dbnav import executer

DIR = os.path.dirname(__file__)
RESOURCES = os.path.join(DIR, '../resources')
SELECT_1 = os.path.join(RESOURCES, 'select-1.sql')


def test_executer():
    os.environ['UNITTEST'] = 'True'
    for test in load():
        yield test,
    del os.environ['UNITTEST']


class ExecuterTestCase(DbTestCase):
    def test_unknown_table(self):
        """Tests unknown tables"""

        self.assertRaises(
            Exception,
            executer.run,
            ['dbnav.sqlite', '-s', 'select 1']
        )

    def test_writer(self):
        """Tests the writer"""

        import sys
        sys.argv = ['']

        self.assertRaises(
            SystemExit,
            self.mute_stderr(executer.main)
        )

        self.assertEqual(
            0,
            executer.main(['dbnav.sqlite/user?id=1', '-s', 'select 1'])
        )
        self.assertEqual(
            -1,
            executer.main(
                ['dbnav.sqlite/user?id=1', '-s', 'select * from unknown'])
        )

    def test_exception(self):
        """Tests exceptions"""

        self.assertRaises(
            OperationalError,
            executer.run,
            ['dbnav.sqlite/', '-s', 'select * from unkown']
        )

    def test_isolation(self):
        """Tests the --isolate-statements option"""

        self.assertEqual(
            0,
            executer.main([
                'dbnav.sqlite/user',
                '--isolate-statements',
                '--mute-errors',
                '-s',
                'select blub; select 1;'
            ])
        )

    def test_empty_statements(self):
        """Tests empty statements"""

        self.assertEqual(
            0,
            executer.main([
                'dbnav.sqlite/user',
                '-s',
                '      '
            ])
        )

    def test_infile(self):
        """Tests reading statements from file"""

        self.assertEqual(
            0,
            executer.main([
                'dbnav.sqlite/user',
                SELECT_1
            ])
        )
