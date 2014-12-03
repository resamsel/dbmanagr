#!/usr/bin/env python
# -*- coding: utf-8 -*-

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
