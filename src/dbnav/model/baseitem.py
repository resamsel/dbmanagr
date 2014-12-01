#!/usr/bin/env python
# -*- coding: utf-8 -*-

from dbnav.formatter import Formatter
from dbnav.utils import hash


class BaseItem:
    def title(self):
        return 'Title'

    def subtitle(self):
        return 'Subtitle'

    def autocomplete(self):
        return 'Autocomplete'

    def validity(self):
        return True

    def icon(self):
        return 'images/icon.png'

    def value(self):
        return self.title()

    def uid(self):
        return hash(self.autocomplete())

    def format(self):
        return Formatter.format(self)
