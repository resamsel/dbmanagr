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

import unittest
import os
import sys

from tests.mock.sources import MockSource
from tests.generator import generator, params

__test__ = False


def create_test(pkg, command, dir, tc, parameters=None):
    test_name = 'test_%s_%s' % (command, tc.replace('-', '_'))
    test = generator(pkg, command, dir, tc, parameters)
    test.__doc__ = 'Params: "%s"' % params(dir, tc)
    test.__name__ = test_name
    test.name = test_name
    return test


class ParentTestCase(unittest.TestCase):
    @classmethod
    def setup_class(cls):
        os.environ['UNITTEST'] = 'True'
        cls.set_up_class()

    @classmethod
    def teardown_class(cls):
        cls.tear_down_class()
        del os.environ['UNITTEST']

    @classmethod
    def set_up_class(cls):
        pass

    @classmethod
    def tear_down_class(cls):
        pass

    @classmethod
    def setup(self):  # noqa
        self.maxDiff = None

    def mute_stderr(self, f):
        def wrapper(*args, **kwargs):
            devnull = open(os.devnull, 'w')
            stderr, sys.stderr = sys.stderr, devnull
            try:
                return f(*args, **kwargs)
            finally:
                sys.stderr.close()
                sys.stderr = stderr

        return wrapper


class DbTestCase(ParentTestCase):
    connection = None

    @classmethod
    def set_up_class(cls):
        DbTestCase.connection = MockSource().list()[1]
        DbTestCase.connection.connect()

    @classmethod
    def tear_down_class(cls):
        DbTestCase.connection.close()
        DbTestCase.connection = None
