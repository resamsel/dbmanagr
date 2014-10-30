#!/usr/bin/env python
# -*- coding: utf-8 -*-

from .baseitem import BaseItem

OPTION_URI_DATABASE_FORMAT = '%s/'

class Database(BaseItem):
    """The database used with the given connection"""

    def __init__(self, connection, name):
        self.connection = connection
        self.name = name

    def __repr__(self):
        return '%s@%s/%s' % (self.connection.user, self.connection.host, self.name)

    def title(self):
        return self.autocomplete()

    def subtitle(self):
        return 'Database'

    def autocomplete(self):
        """Retrieves the autocomplete string"""

        return OPTION_URI_DATABASE_FORMAT % (self.__repr__())

    def icon(self):
        return 'images/database.png'
