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

import sys
import BaseHTTPServer
import json
import urllib2

from json import JSONEncoder

from dbnav import navigator, exporter, differ, executer, grapher
from dbnav.writer import Writer
from dbnav.json import Jsonable
from dbnav.node import BaseNode

COMMANDS = {
    'navigator': navigator,
    'exporter': exporter,
    'differ': differ,
    'executer': executer,
    'grapher': grapher
}


class Encoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Jsonable):
            return obj.as_json()
        return as_json(obj)


class DaemonHTTPRequestHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    def do_POST(self):
        parts = self.path.split('/')
        command = parts[1]
        if command not in COMMANDS:
            self.send_error(404)
            return

        args = json.loads(self.rfile.read(
            int(self.headers.getheader('content-length'))))

        try:
            items = COMMANDS[command].execute(args)
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(items, cls=Encoder))
        except BaseException as e:
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({'code':500, 'message':e.message}))

def run(server_class=BaseHTTPServer.HTTPServer,
        handler_class=BaseHTTPServer.BaseHTTPRequestHandler):
    server_address = ('', 8020)
    httpd = server_class(server_address, handler_class)
    httpd.serve_forever()

run(handler_class=DaemonHTTPRequestHandler)
