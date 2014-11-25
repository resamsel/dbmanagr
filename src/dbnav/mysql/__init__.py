#!/usr/bin/env python
# -*- coding: utf-8 -*-

__all__ = ["databaseconnection", "sources"]

from os.path import expanduser
from os import getenv

from dbnav.utils import module_installed
from dbnav.sources import Source
from dbnav.mysql.sources import DBExplorerMySQLSource, MypassSource
from dbnav.options import Options
from dbnav.mysql.options import MySQLOptionsParser

DRIVERS = {
    'MySQLdb': 'mysqldb'
}


def init_mysql(driver, dbexplorer_config, mypass_config):
    Source.sources.append(DBExplorerMySQLSource(driver, dbexplorer_config))
    Source.sources.append(MypassSource(driver, mypass_config))


def init():
    module = module_installed(*DRIVERS.keys())
    if not module:
        return

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
