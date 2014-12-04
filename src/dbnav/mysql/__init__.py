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

__all__ = ["databaseconnection", "sources"]

from os.path import expanduser
from os import getenv
from collections import OrderedDict

from dbnav import __drivers__
from dbnav.utils import module_installed
from dbnav.sources import Source
from dbnav.mysql.sources import DBExplorerMySQLSource, MypassSource
from dbnav.options import Options
from dbnav.mysql.options import MySQLOptionsParser

DRIVERS = OrderedDict([
    ('MySQLdb', 'mysql+mysqldb://{user}:{password}@{host}/{database}'
                '?charset=utf8&use_unicode=0'),
    ('oursql', 'mysql+oursql://{user}:{password}@{host}/{database}'),
    ('pymysql', 'mysql+pymysql://{user}:{password}@{host}/{database}'),
])


def init_mysql(driver, dbexplorer_config, mypass_config):
    Source.sources.append(DBExplorerMySQLSource(driver, dbexplorer_config))
    Source.sources.append(MypassSource(driver, mypass_config))


def init():
    module = module_installed(*DRIVERS.keys())
    if not module:
        return

    __drivers__.append(module)
    init_mysql(
        DRIVERS[module],
        getenv(
            'DBEXPLORER_CFG',
            expanduser('~/.dbexplorer/dbexplorer.cfg')),
        getenv(
            'PGPASS_CFG',
            expanduser('~/.mypass'))
    )

    Options.parser['mysql'] = MySQLOptionsParser()
