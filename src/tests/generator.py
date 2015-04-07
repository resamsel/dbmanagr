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

from os import path, makedirs, environ
from nose.tools import assert_equal
import codecs

from dbnav.writer import Writer

LOGFILE = '{}/target/dbnavigator.log'.format(
    path.join(path.dirname(__file__), '..', '..'))


def params(dir, testcase):
    with codecs.open(
            path.join(dir, 'resources', testcase),
            encoding='utf-8',
            mode='r') as f:
        return map(lambda line: line.strip(), f.readlines())


def expected(dir, testcase):
    with codecs.open(
            path.join(dir, 'resources', 'expected', testcase),
            encoding='utf-8',
            mode='r') as f:
        return f.read()


def write_actual(command, testcase, content):
    try:
        makedirs(path.join('target', 'actual', command))
    except BaseException:
        pass
    with codecs.open(
            path.join('target', 'actual', command, testcase),
            encoding='utf-8',
            mode='w') as f:
        f.write(content)
    return content


def update_expected(dir, testcase, content):
    with codecs.open(
            path.join(dir, 'resources', 'expected', testcase),
            encoding='utf-8',
            mode='w') as f:
        f.write(content)
    return content


def generator(f, command, dir, tc, parameters=None):
    if parameters is None:
        parameters = []

    assert_equal.im_class.maxDiff = None

    def test():
        environ['DBNAV_INPUT'] = path.join(dir, 'resources', tc)
        p, e = params(dir, tc), expected(dir, tc)
        items = f.run([
            '--debug',
            '-L', LOGFILE] + parameters + p)
        actual = Writer.write(items)
        write_actual(command, tc, actual)

        # WARNING: this is code that creates the expected output - only
        # uncomment when in need!
        # e = update_expected(dir, tc, actual)

        assert_equal(e, actual)
    return test
