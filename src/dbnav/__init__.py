#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from dbnav.writer import Writer

__all__ = ["navigator", "item", "writer", "sources", "querybuilder", "logger", "options", "tests"]

def wrapper(f):
    try:
        print Writer.write(f(sys.argv))
    except (SystemExit, KeyboardInterrupt) as e:
        sys.exit(-1)
    except BaseException as e:
        sys.stderr.write('{0}: {1}\n'.format(sys.argv[0].split('/')[-1], e))
        raise

