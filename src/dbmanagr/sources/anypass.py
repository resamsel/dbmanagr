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

from os.path import isfile, abspath

from dbmanagr.sources.source import Source

logger = logging.getLogger(__name__)


class AnyPassSource(Source):
    def __init__(self, driver, file_, con_creator):
        Source.__init__(self)
        self.driver = driver
        self.file = file_
        self.con_creator = con_creator

    def list(self):
        if not isfile(self.file):
            from os.path import realpath
            logger.info(
                'File %r does not exist (this file: %r)',
                self.file, realpath(__file__))

            return self._connections

        if not self._connections:
            with open(self.file) as f:
                anypass = f.readlines()

            for line in anypass:
                connection = self.con_creator(
                    self.driver, *line.strip().split(':'))
                self._connections.append(connection)

        logger.debug('Connections: %s', self._connections)

        return self._connections


class AnyFilePassSource(AnyPassSource):
    def list(self):
        if not isfile(self.file):
            from os.path import realpath
            logger.info(
                'File %r does not exist (this file: %r)',
                self.file, realpath(__file__))

            return self._connections

        if not self._connections:
            with open(self.file) as f:
                anypass = f.readlines()

            for line in anypass:
                filepath = abspath(line.strip())
                if isfile(filepath):
                    connection = self.con_creator(
                        self.driver, None, None, filepath, None, None)
                    self._connections.append(connection)

        logger.debug('Connections: %s', self._connections)

        return self._connections
