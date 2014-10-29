#!/usr/bin/env python
# -*- coding: utf-8 -*-

__all__ = ["databaseconnection", "sources"]

from os.path import expanduser
from os import getenv

from ..sources import Source
from .sources import DBExplorerMySQLSource
from ..options import Options
from .options import MySQLOptionsParser

def init_mysql(dbexplorer_config):
    Source.sources.append(DBExplorerMySQLSource(dbexplorer_config))

init_mysql(
    getenv('DBEXPLORER_CFG',
        expanduser('~/.dbexplorer/dbexplorer.cfg'))
)

Options.parser['mysql'] = MySQLOptionsParser()
