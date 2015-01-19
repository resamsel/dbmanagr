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

from dbnav.jsonable import Jsonable
from dbnav.formatter import Formatter
from dbnav import utils


def freeze(d):
    if isinstance(d, dict):
        return frozenset((key, freeze(value)) for key, value in d.items())
    elif isinstance(d, list):
        return tuple(freeze(value) for value in d)
    return d


class Dto(Jsonable):
    def __init__(
            self,
            title=None,
            subtitle=None,
            autocomplete=None,
            uid=None,
            icon=None):
        self.title_ = title
        self.subtitle_ = subtitle
        self.autocomplete_ = autocomplete
        self.uid_ = uid
        self.icon_ = icon

    def autocomplete(self):
        return self.autocomplete_

    def __hash__(self):
        return hash(freeze(self.__dict__))

    def __eq__(self, o):
        return hash(self) == hash(o)

    def title(self):
        return self.title_

    def subtitle(self):
        return self.subtitle_

    def value(self):
        return self.title()

    def validity(self):
        return True

    def uid(self):
        if self.uid_ is not None:
            return self.uid_
        return utils.hash(self.autocomplete())

    def icon(self):  # pragma: no cover
        if self.icon_ is not None:
            return self.icon_
        return 'images/icon.png'

    def format(self):
        return Formatter.format(self)
