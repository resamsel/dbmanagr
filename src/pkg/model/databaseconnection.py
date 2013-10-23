#!/usr/bin/env python
# -*- coding: utf-8 -*-

class Row:
    columns = {'id': 1, 'title': 'Title', 'subtitle': 'Subtitle', 'column_name': 'column', 0: '0', 1: '1', 'column': 'col'}
    def __init__(self, *args):
        if len(args) > 0:
            self.columns = args[0]
            if 'id' not in self.columns:
                self.columns['id'] = 0
        else:
            self.columns = Row.columns
    def __getitem__(self, i):
        return self.columns[i]
    def __contains__(self, item):
        return item in self.columns

class Cursor:
    def execute(self, query):
        pass
    def fetchone(self):
        return Row()
    def fetchall(self):
        return [Row()]

class DatabaseConnection:
    def __init__(self, *args):
        pass

    def title(self):
        return 'Title'

    def subtitle(self):
        return 'Subtitle'

    def autocomplete(self):
        return 'Autocomplete'

    def matches(self, s):
        return s in self.title()

    def connect(self, database):
        pass

    def connected(self):
        return True

    def close(self):
        pass

    def cursor(self):
        return Cursor()

    def databases(self):
        return []

    def tables(self):
        return {}

    def __str__(self):
        return self.__repr__()

    def __eq__(self, other):
        return self.__repr__() == other.__repr__()

    def __hash__(self):
        return hash(self.__repr__())

    def __getstate__(self):
        state = dict(self.__dict__)
        logging.debug('State: %s' % state)
        if 'con' in state:
            del state['con']
        return state
