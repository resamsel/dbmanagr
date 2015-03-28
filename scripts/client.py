#!/usr/bin/env python
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

import json
import dbnav
import urllib2
import sys

from dbnav.config import Config
from dbnav.exporter import parser
from dbnav.exporter.writer import SqlInsertWriter

try:
    response = urllib2.urlopen(
        'http://localhost:8020/exporter',
        json.dumps(sys.argv[1:]))

    o = dbnav.json.from_json(json.load(response))
    print SqlInsertWriter(Config.init(sys.argv[:1], parser)).write(o)
except urllib2.HTTPError as e:
    print dbnav.json.from_json(json.load(e))
except urllib2.URLError as e:
    print 'Daemon not available', e
except BaseException as e:
    print e.__class__, e
    import pdb
    _type, value, tb = sys.exc_info()  # pragma: no cover
    # traceback.print_exc()
    pdb.post_mortem(tb)  # pragma: no cover
