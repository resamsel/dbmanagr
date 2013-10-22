#!/usr/bin/env python
# -*- coding: utf-8 -*-

VALID = "yes"
INVALID = "no"

IMAGE_CONNECTION = 'images/connection.png'
IMAGE_DATABASE = 'images/database.png'
IMAGE_TABLE = 'images/table.png'
IMAGE_ROW = 'images/row.png'
IMAGE_VALUE = 'images/value.png'
IMAGE_FOREIGN_KEY = 'images/foreign-key.png'
IMAGE_FOREIGN_VALUE = 'images/foreign-value.png'

OPTION_URI_FORMAT = '%s@%s/%s'
OPTION_URI_TABLES_FORMAT = '%s/%s/'
OPTION_URI_ROW_FORMAT = '%s/%s/%s'

ROW_QUERY_FORMAT = """
select
        column_name
    from
        INFORMATION_SCHEMA.COLUMNS
    where
        table_name = '%s'
"""
