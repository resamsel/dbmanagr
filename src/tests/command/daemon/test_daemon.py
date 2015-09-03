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

from tests.command.daemon import load
from tests.testcase import ParentTestCase
from dbnav.command import daemon
from dbnav.utils import mute_stderr


def test_daemon():
    os.environ['UNITTEST'] = 'True'
    for test in load():
        yield test,
    del os.environ['UNITTEST']


class DaemonTestCase(ParentTestCase):
    def test_writer(self):
        """Tests the writer"""

        import sys
        sys.argv = ['']

        self.assertRaises(
            SystemExit,
            mute_stderr(daemon.main)
        )
        self.assertRaises(
            SystemExit,
            mute_stderr(daemon.main),
            []
        )
        self.assertIsNone(daemon.main(['stop']))

    def test_main(self):
        """Tests the main function"""

        self.assertIsNone(daemon.main(['status']))
        self.assertIsNone(daemon.main(['stop']))
