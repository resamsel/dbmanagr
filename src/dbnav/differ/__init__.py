#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

from dbnav.writer import Writer

from dbnav import decorator
from dbnav.config import Config
from dbnav.sources import Source
from .args import parser
from .writer import DiffWriter


def column_ddl(c):
    return c.ddl()


def column_name(c):
    return c.name


class DatabaseDiffer:
    """The main class"""

    @staticmethod
    def diff(left, right):
        """The main method that splits the arguments and starts the magic"""

        lcon = Source.connection(left)
        if not lcon:
            raise Exception('Could not find connection {0}'.format(left.uri))
        lopts = left.get(lcon.driver)
        rcon = Source.connection(right)
        if not rcon:
            raise Exception('Could not find connection {0}'.format(right.uri))
        ropts = right.get(rcon.driver)

        try:
            lcon.connect(lopts.database)
            rcon.connect(ropts.database)
            ltables = lcon.tables()
            if lopts.table not in ltables:
                raise Exception(
                    "Could not find table '{0}' in left connection".format(
                        lopts.table))
            ltable = ltables[lopts.table]
            rtables = rcon.tables()
            if ropts.table not in rtables:
                raise Exception(
                    "Could not find table '{0}' in right connection".format(
                        ropts.table))
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

            return map(lambda (k, v): v, r.iteritems())
        finally:
            lcon.close()
            rcon.close()


def main():
    run(sys.argv)


@decorator
def run(argv):
    left = Config.init(argv, parser)
    left.uri = left.left
    left.update_parsers()
    right = Config.init(argv, parser)
    right.uri = right.right
    right.update_parsers()

    if left.formatter:
        Writer.set(left.formatter(left, right))
    else:
        Writer.set(DiffWriter(left, right))

    return DatabaseDiffer.diff(left, right)

if __name__ == "__main__":
    main()
