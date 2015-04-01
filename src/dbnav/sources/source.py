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

logger = logging.getLogger(__name__)


class Source(object):
    sources = []

    def __init__(self):
        self._connections = []

    def list(self):
        return self._connections

    @staticmethod
    def connections():
        cons = []
        for source in Source.sources:
            cons += source.list()
        return set(cons)

    @staticmethod
    def connection(options):
        # search exact match of connection
        for connection in Source.connections():
            opts = options.get(connection.dbms)
            if connection.matches(opts):
                return connection
        return None
