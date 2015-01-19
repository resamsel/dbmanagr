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

from dbnav.dto import Dto
from dbnav.jsonable import from_json
from dbnav.utils import filter_keys


class Item(Dto):
    def __init__(
            self,
            title=None,
            subtitle=None,
            autocomplete=None,
            validity=None,
            icon=None,
            value=None,
            uid=None,
            format=None):
        Dto.__init__(self, title, subtitle, autocomplete)

        self.validity_ = validity
        self.icon_ = icon
        self.value_ = value
        self.uid_ = uid
        self.format_ = format

    def __str__(self):
        return self.title()

    def title(self):
        return self.title_

    def subtitle(self):
        return self.subtitle_

    def autocomplete(self):
        return self.autocomplete_

    def validity(self):
        return self.validity_

    def icon(self):
        return self.icon_

    def value(self):
        return self.value_

    def uid(self):
        return self.uid_

    def format(self):
        return self.format_

    @staticmethod
    def from_json(d):
        return Item(
            **from_json(
                filter_keys(
                    d,
                    'title', 'subtitle', 'autocomplete', 'validity', 'icon',
                    'value', 'uid', 'format'
                )
            )
        )
