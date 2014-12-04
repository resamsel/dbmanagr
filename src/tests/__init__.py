#!/usr/bin/env python
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

from tests import navigator, grapher, exporter, differ
from tests import utils, comment, querybuilder, options, logger, exception
from tests.model import row
from tests.sqlite import sources as sqlite_sources
from tests.postgresql import sources as postgresql_sources
from tests.mysql import sources as mysql_sources


def load_suite():
    suite = unittest.TestSuite()

    suite.addTest(utils.load_suite())
    suite.addTest(comment.load_suite())
    suite.addTest(querybuilder.load_suite())
    suite.addTest(options.load_suite())
    suite.addTest(logger.load_suite())
    suite.addTest(exception.load_suite())

    suite.addTest(row.load_suite())

    suite.addTest(sqlite_sources.load_suite())
    suite.addTest(postgresql_sources.load_suite())
    suite.addTest(mysql_sources.load_suite())

    suite.addTest(navigator.load_suite())
    suite.addTest(grapher.load_suite())
    suite.addTest(exporter.load_suite())
    suite.addTest(differ.load_suite())

    return suite
