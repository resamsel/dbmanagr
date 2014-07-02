#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
from ..item import Item

logger = logging.getLogger(__name__)

class BaseItem:
    def title(self):
        return 'Title'
    def subtitle(self):
        return 'Subtitle'
    def autocomplete(self):
        return 'Autocomplete'
    def validity(self):
        return 'yes'
    def icon(self):
        return 'images/icon.png'
    def item(self):
        return Item(self.title(),
            self.subtitle(),
            self.autocomplete(),
            self.validity(),
            self.icon())
