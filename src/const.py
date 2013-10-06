#!/usr/local/bin/python
# -*- coding: utf-8 -*-

ITEMS_FORMAT = '<items>{0}</items>'
ITEM_FORMAT = """
    <item uid="{0}" arg="{2}" autocomplete="{1}">
        <title>{2}</title>
        <subtitle>{3}</subtitle>
        <icon>{4}</icon>
    </item>
"""

IMAGE_CONNECTION = 'images/connection.png'
IMAGE_DATABASE = 'images/database.png'
IMAGE_TABLE = 'images/table.png'
IMAGE_ROW = 'images/row.png'
IMAGE_VALUE = 'images/value.png'

OPTION_URI_FORMAT = '%s@%s/%s'
OPTION_URI_DATABASE_FORMAT = '%s/'
OPTION_URI_TABLES_FORMAT = '%s/%s/'
OPTION_URI_VALUE_FORMAT = '%s/%s/%s/'

COMMENT_ID = 'id'
COMMENT_TITLE = 'title'
COMMENT_SUBTITLE = 'subtitle'
COMMENT_ORDER_BY = 'order'
COMMENT_SEARCH = 'search'
COMMENT_DISPLAY = 'display'

ID_FORMAT = "{0}.id"
JOIN_FORMAT = """
        left outer join \"{0}\" {1} on {1}.{2} = {3}.{4}"""

DATABASES_QUERY = """
select
        datname as database_name
    from
        pg_database
    where
        datistemplate = false
    order by datname
"""
FOREIGN_KEY_QUERY_FORMAT = """
select
        tc.constraint_name,
        tc.table_name,
        kcu.column_name,
        ccu.table_name foreign_table_name,
        ccu.column_name foreign_column_name
    from
        information_schema.table_constraints tc
        join information_schema.key_column_usage kcu ON tc.constraint_name = kcu.constraint_name
        join information_schema.constraint_column_usage ccu ON ccu.constraint_name = tc.constraint_name
    where
        constraint_type = 'FOREIGN KEY'
         and tc.table_name = '%s'
"""
ROW_QUERY_FORMAT = """
select
        column_name
    from
        INFORMATION_SCHEMA.COLUMNS
    where
        table_name = '%s'
"""
TABLES_QUERY = """
select
        t.table_name as tbl, obj_description(c.oid) as comment
    from information_schema.tables t,
        pg_class c
    where
        table_schema = 'public'
        and t.table_name = c.relname
        and c.relkind = 'r'
    order by t.table_name
"""
