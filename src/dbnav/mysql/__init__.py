#!/usr/bin/env python
# -*- coding: utf-8 -*-

__all__ = ["databaseconnection", "sources"]

from os.path import expanduser
from os import getenv

from dbnav.sources import Source
from dbnav.mysql.sources import DBExplorerMySQLSource, MypassSource
from dbnav.options import Options
from dbnav.mysql.options import MySQLOptionsParser


def init_mysql(dbexplorer_config, mypass_config):
    Source.sources.append(DBExplorerMySQLSource(dbexplorer_config))
    Source.sources.append(MypassSource(mypass_config))

init_mysql(
    getenv(
        'DBEXPLORER_CFG',
        expanduser('~/.dbexplorer/dbexplorer.cfg')),
    getenv(
        'PGPASS_CFG',
        expanduser('~/.mypass'))
)

Options.parser['mysql'] = MySQLOptionsParser()
