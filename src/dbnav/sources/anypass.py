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

from os.path import isfile, abspath

from dbnav.sources import Source


class AnyPassSource(Source):
    def __init__(self, driver, file, con_creator):
        Source.__init__(self)
        self.driver = driver
        self.file = file
        self.con_creator = con_creator

    def list(self):
        if not isfile(self.file):
            return self.connections
        if not self.connections:
            with open(self.file) as f:
                anypass = f.readlines()

            for line in anypass:
                connection = self.con_creator(
                    self.driver, *line.strip().split(':'))
                self.connections.append(connection)

        return self.connections


class AnyFilePassSource(AnyPassSource):
    def list(self):
        if not isfile(self.file):
            return self.connections
        if not self.connections:
            with open(self.file) as f:
                anypass = f.readlines()

            for line in anypass:
                filepath = abspath(line.strip())
                if isfile(filepath):
                    connection = self.con_creator(
                        self.driver, None, None, filepath, None, None)
                    self.connections.append(connection)

        return self.connections
