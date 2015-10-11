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

from dbmanagr.writer import FormatWriter
from dbmanagr.formatter import Formatter, DefaultFormatter


class ArgumentWriter(FormatWriter):
    def __init__(self, options=None):
        FormatWriter.__init__(self, u'{0}\n', u'{0}\n')
        self.options = options
        Formatter.set(DefaultFormatter())

    def str(self, items):
        options = self.options
        (includes, excludes, substitutes) = items
        output = []
        if options.includes and len(includes) > 0:
            output.append(u'-i {0}'.format(','.join(includes)))
        if options.excludes and len(excludes) > 0:
            output.append(u'-x {0}'.format(','.join(excludes)))
        if options.substitutes and len(substitutes) > 0:
            output.append(u'-s {0}'.format(','.join(substitutes)))
        return self.items_format.format(' '.join(output))


class ArgumentVerboseWriter(FormatWriter):
    def __init__(self, options=None):
        FormatWriter.__init__(self, u'{0}\n', u'{0}')
        if options.verbose > 0:
            Formatter.set(DefaultFormatter())
        else:
            Formatter.set(DefaultFormatter())

    def str(self, items):
        (includes, excludes, substitutes) = items
        output = []
        if len(includes) > 0:
            output.append('Includes:\n{0}\n\n'.format('\n'.join(
                map(lambda x: ' - {0}'.format(x), includes))))
        if len(excludes) > 0:
            output.append('Excludes:\n{0}\n\n'.format('\n'.join(
                map(lambda x: ' - {0}'.format(x), excludes))))
        if len(substitutes) > 0:
            output.append('Substitutes:\n{0}'.format('\n'.join(
                map(lambda x: ' - {0}'.format(x), substitutes))))
        return self.items_format.format(''.join(output))


class ArgumentTestWriter(ArgumentWriter):
    pass
