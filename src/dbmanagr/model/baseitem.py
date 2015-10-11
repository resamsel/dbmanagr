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

import logging

from dbmanagr.formatter import Formatter
from dbmanagr.model import Model
from dbmanagr.logger import LogWith
from dbmanagr.utils import hash_

logger = logging.getLogger(__name__)


class BaseItem(Model):
    def title(self):  # pragma: no cover
        return 'Title'

    def subtitle(self):  # pragma: no cover
        return 'Subtitle'

    def autocomplete(self):  # pragma: no cover
        return 'Autocomplete'

    def validity(self):
        return True

    def icon(self):  # pragma: no cover
        return 'images/icon.png'

    def value(self):
        return self.title()

    @LogWith(logger)
    def uid(self):
        return hash_(self.autocomplete())

    def format(self):
        return Formatter.format(self)
