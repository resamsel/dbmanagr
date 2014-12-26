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

import logging

from urlparse import urlparse

from dbnav.logger import LogWith
from dbnav.options import parse_filter, restriction

logger = logging.getLogger(__name__)


class SQLiteDriver:
    def get(self, driver):
        return self

    @LogWith(logger)
    def restriction(self, *args):
        return restriction(*args)

    def __repr__(self):
        return str(self.__dict__)


class SQLiteOptionsParser:
    def parse(self, source):
        driver = SQLiteDriver()
        driver.__dict__.update(source.__dict__)
        if driver.uri:
            uri = driver.uri
            url = urlparse('sqlite://%s' % uri)
            paths = url.path.split('/')

            if len(paths) > 1:
                driver.table = paths[1]
            if '?' in uri:
                driver.filter = parse_filter(url.query)
                paths.append(url.query)

            driver.show = {
                1: 'connections',
                2: 'tables',
                3: 'columns',
                4: 'values'
            }.get(len(paths), 'connections')

        return driver
