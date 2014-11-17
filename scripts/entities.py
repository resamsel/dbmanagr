#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm.session import Session
from sqlalchemy.orm import aliased
from sqlalchemy.sql.expression import label

url = 'sqlite+pysqlite:///{pwd}/src/tests/resources/dbnav-c.sqlite'.format(
    pwd=os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

engine = create_engine(url)
c = engine.connect()
meta = MetaData()
meta.reflect(bind=engine)

article = aliased(meta.tables['article'], name='_article')
user = aliased(meta.tables['user'], name='_user')
blog_user = aliased(meta.tables['blog_user'], name='_blog_user')
blog = aliased(meta.tables['blog'], name='_blog')

session = Session(engine)
query = session\
    .query(
        *map(
            lambda col: col.label('{}_{}'.format(col.table.name, col.name)),
            reduce(
                lambda x, y: x + list(y.columns), [blog, user], [])))\
    .join(blog_user)\
    .join(user)\
    .filter(user.columns['username'] == 'mpierce71')

print query
all = query.all()
print all
for r in all:
    print r.__dict__
