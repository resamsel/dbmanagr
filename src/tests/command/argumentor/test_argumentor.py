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

from tests.command.argumentor import load
from tests.testcase import DbTestCase
from dbmanagr.command import argumentor
from dbmanagr.utils import mute_stderr


def test_argumentor():
    os.environ['UNITTEST'] = 'True'
    for test in load():
        yield test,
    del os.environ['UNITTEST']


class ArgumentorTestCase(DbTestCase):
    def test_writer(self):
        """Tests the writer"""

        import sys
        sys.argv = ['', 'unknown']

        self.assertRaises(
            SystemExit,
            mute_stderr(argumentor.main),
            ['unknown']
        )
        self.assertRaises(
            SystemExit,
            mute_stderr(argumentor.main)
        )

        self.assertEqual(
            0,
            argumentor.main(['tests/command/argumentor/resources/empty.yaml'])
        )

    def test_execute(self):
        """Tests the argumentor.execute function"""

        self.assertRaises(
            SystemExit,
            mute_stderr(argumentor.execute),
            ['unknown']
        )
