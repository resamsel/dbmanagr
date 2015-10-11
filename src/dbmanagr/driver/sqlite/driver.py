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

from dbmanagr.logger import LogWith
from dbmanagr.options import restriction, FileOptionsParser
from dbmanagr.driver import DatabaseDriver

logger = logging.getLogger(__name__)


class SQLiteDriver(DatabaseDriver):
    @LogWith(logger)
    def restriction(self, *args):
        return restriction(*args)

    def statement_activity(self, con):
        return []

    def __repr__(self):
        return str(self.__dict__)


class SQLiteOptionsParser(FileOptionsParser):
    def create_driver(self):
        return SQLiteDriver()
