#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import logging

from main.dbnavigator import *
from main.sources import *
from main.sqlite.sources import *
from main.postgresql.sources import *

logger = logging.getLogger(__name__)

Source.sources = []
Source.sources.append(DBExplorerPostgreSQLSource('build/testfiles/resources/dbexplorer.cfg'))
Source.sources.append(PgpassSource('build/testfiles/resources/pgpass'))
Source.sources.append(DBExplorerSQLiteSource('build/testfiles/resources/dbexplorer.cfg'))

main()

logger.info('Working dir: %s', os.getcwd())
