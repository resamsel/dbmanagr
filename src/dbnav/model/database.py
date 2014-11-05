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
        return '{user}@{host}/{database}'.format(
            user=self.connection.user,
            host=self.connection.host,
            database=self.name)

    def title(self):
        return self.autocomplete()

    def subtitle(self):
        return 'Database'

    def autocomplete(self):
        """Retrieves the autocomplete string"""

        return OPTION_URI_DATABASE_FORMAT % (self.__repr__())

    def icon(self):
        return 'images/database.png'
