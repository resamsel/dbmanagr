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

from dbmanagr.writer import Writer

from dbmanagr.wrapper import Wrapper
from dbmanagr.config import Config
from dbmanagr.sources.source import Source
from dbmanagr.exception import UnknownTableException, \
    UnknownConnectionException
from dbmanagr.dto.mapper import to_dto

from .args import parser
from .writer import DiffWriter


def column_ddl(c):
    return c.ddl()


def column_name(c):
    return c.name


class DatabaseDiffer(Wrapper):
    """The main class"""
    def __init__(self, left, right):
        Wrapper.__init__(self, left)

        self.left = left
        self.right = right

        if left.formatter:
            Writer.set(left.formatter(left, right))
        else:
            Writer.set(DiffWriter(left, right))

    def execute(self):
        """The main method that splits the arguments and starts the magic"""
        left, right = self.left, self.right

        lcon = Source.connection(left)
        if not lcon:
            raise UnknownConnectionException(
                left.uri,
                map(lambda c: c.autocomplete(), Source.connections()))
        lopts = left.get(lcon.dbms)
        rcon = Source.connection(right)
        if not rcon:
            raise UnknownConnectionException(
                right.uri,
                map(lambda c: c.autocomplete(), Source.connections()))
        ropts = right.get(rcon.dbms)

        try:
            lcon.connect(lopts.database)
            rcon.connect(ropts.database)
            ltables = lcon.tables()
            if lopts.table not in ltables:
                raise UnknownTableException(lopts.table, ltables.keys())
            ltable = ltables[lopts.table]
            rtables = rcon.tables()
            if ropts.table not in rtables:
                raise UnknownTableException(ropts.table, rtables.keys())
            rtable = rtables[ropts.table]

            lcols = map(
                column_ddl if left.compare_ddl else column_name,
                ltable.columns())
            rcols = map(
                column_ddl if right.compare_ddl else column_name,
                rtable.columns())

            lplus = dict(map(
                lambda c: (c.split()[0], ltable.column(c.split()[0])),
                list(set(lcols) - set(rcols))))
            rplus = dict(map(
                lambda c: (c.split()[0], rtable.column(c.split()[0])),
                list(set(rcols) - set(lcols))))

            r = {}
            for k, v in lplus.iteritems():
                if k in rplus:
                    r[k] = (v, rplus[k])
                else:
                    r[k] = (v, None)
            for k, v in rplus.iteritems():
                if k not in lplus:
                    r[k] = (None, v)

            return to_dto(map(lambda (k, v): v, r.iteritems()))
        finally:
            lcon.close()
            rcon.close()


def init(argv, parser):
    left = Config.init(argv, parser)
    left.uri = left.left
    left.update_parsers()
    right = Config.init(argv, parser)
    right.uri = right.right
    right.update_parsers()
    return (left, right)


def execute(args):
    """
    Directly calls the execute method and avoids using the wrapper
    """
    return DatabaseDiffer(*init(args, parser)).execute()


def run(args):
    return DatabaseDiffer(*init(args, parser)).run()


def main(args=None):
    if args is None:
        args = sys.argv[1:]
    return DatabaseDiffer(*init(args, parser)).write()
