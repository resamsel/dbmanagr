#!/usr/bin/env python
# -*- coding: utf-8 -*-

from .baseitem import BaseItem
from dbnav import KIND_FOREIGN_VALUE, KIND_FOREIGN_KEY, KIND_VALUE
from dbnav import IMAGE_FOREIGN_VALUE, IMAGE_FOREIGN_KEY, IMAGE_VALUE

TITLES = {
    KIND_FOREIGN_VALUE: u'← %s',
    KIND_FOREIGN_KEY: u'→ %s',
    KIND_VALUE: u'%s'
}
ICONS = {
    KIND_FOREIGN_VALUE: IMAGE_FOREIGN_VALUE,
    KIND_FOREIGN_KEY: IMAGE_FOREIGN_KEY,
    KIND_VALUE: IMAGE_VALUE
}


class Value(BaseItem):
    """A value from the database"""

    def __init__(self, value, subtitle, autocomplete, validity, kind):
        self._value = value
        self._subtitle = subtitle
        self._autocomplete = autocomplete
        self._validity = validity
        self.kind = kind

    def title(self):
        if type(self._value) is buffer:
            return '[BLOB]'
        return TITLES.get(self.kind, KIND_VALUE) % self._value

    def subtitle(self):
        return self._subtitle

    def autocomplete(self):
        return self._autocomplete

    def validity(self):
        return self._validity

    def icon(self):
        return ICONS.get(self.kind, KIND_VALUE)

    def value(self):
        return self._value
