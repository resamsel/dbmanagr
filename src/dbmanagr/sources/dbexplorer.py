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

import xml.etree.ElementTree as ET
from urlparse import urlparse
from os.path import isfile

from dbmanagr.sources.source import Source

logger = logging.getLogger(__name__)


class DBExplorerSource(Source):
    def __init__(self, driver, file_, scheme, con_creator):
        Source.__init__(self)
        self.driver = driver
        self.file = file_
        self.scheme = scheme
        self.con_creator = con_creator

    def list(self):
        if not isfile(self.file):
            from os.path import realpath
            logger.warn(
                'File %r does not exist (this file: %r)',
                self.file, realpath(__file__))

            return self._connections

        if not self._connections:
            try:
                tree = ET.parse(self.file)
            except Exception as e:
                logger.warn(
                    'Error parsing dbExplorer config file: %s', e.message)
                return []
            root = tree.getroot()
            for c in root.iter('connection'):
                url = urlparse(c.find('url').text.replace('jdbc:', ''))
                if url.scheme == self.scheme:
                    host = url.netloc.split(':')[0]
                    port = 3306
                    database = '*'
                    usernode = c.find('user')
                    if usernode is not None:
                        user = usernode.text
                    else:
                        user = None
                    passwordnode = c.find('password')
                    if passwordnode is not None:
                        password = passwordnode.text
                    else:
                        password = None
                    connection = self.con_creator(
                        self.driver, host, port, database, user, password)
                    self._connections.append(connection)

        return self._connections
