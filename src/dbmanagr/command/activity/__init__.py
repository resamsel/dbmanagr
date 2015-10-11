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

import sys
import logging

from dbmanagr.wrapper import Wrapper
from dbmanagr.config import Config
from dbmanagr.sources.source import Source
from dbmanagr.writer import Writer
from dbmanagr.dto.mapper import to_dto
from dbmanagr.jsonable import Jsonable, from_json
from dbmanagr.utils.sql import sanitise

from .args import parser
from .writer import StatementActivityWriter

logger = logging.getLogger(__name__)


class RowItem(Jsonable):
    def __init__(self, row):
        self.row = row

    def __hash__(self):
        return hash(self.row.row)

    def __eq__(self, o):
        return hash(self) == hash(o)

    @staticmethod
    def from_json(d):
        return RowItem(
            from_json(d['row'])
        )


class DatabaseStatus(Wrapper):
    def __init__(self, options):
        Wrapper.__init__(self, options)

        if options.formatter:
            Writer.set(options.formatter(options))
        else:
            Writer.set(StatementActivityWriter(options))

    def execute(self):
        options = self.options

        options.pattern = sanitise(options.pattern)

        cons = Source.connections()

        # search exact match of connection
        for connection in cons:
            opts = options.get(connection.dbms)
            if opts.show_code > 1 and connection.matches(opts):
                try:
                    connection.connect(opts.database)
                    return to_dto(map(
                        RowItem, opts.statement_activity(connection)))
                finally:
                    connection.close()

        raise Exception('Specify the complete URI of the connection')


def execute(args):
    """
    Directly calls the execute method and avoids using the wrapper
    """
    return DatabaseStatus(Config.init(args, parser)).execute()


def run(args):
    return DatabaseStatus(Config.init(args, parser)).run()


def main(args=None):
    if args is None:
        args = sys.argv[1:]
    return DatabaseStatus(Config.init(args, parser)).write()
