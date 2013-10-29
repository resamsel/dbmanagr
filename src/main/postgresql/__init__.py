#!/usr/bin/env python
# -*- coding: utf-8 -*-

__all__ = ["databaseconnection", "sources"]

from os.path import expanduser

from ..sources import Source
from .sources import *
from ..options import Options
from .options import *

Source.sources.append(DBExplorerPostgreSQLSource(expanduser('~/.dbexplorer/dbexplorer.cfg')))
Source.sources.append(PgpassSource(expanduser('~/.pgpass')))

Options.parser['postgresql'] = PostgreSQLOptions()
