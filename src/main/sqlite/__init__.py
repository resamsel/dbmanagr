#!/usr/bin/env python
# -*- coding: utf-8 -*-

__all__ = ["databaseconnection", "sources"]

from os.path import expanduser

from ..sources import Source
from .sources import *
from ..options import Options
from .options import *

Source.sources.append(DBExplorerSQLiteSource(expanduser('~/.dbexplorer/dbexplorer.cfg')))

Options.parser['sqlite'] = SQLiteOptions()
