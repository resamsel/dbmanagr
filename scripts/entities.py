#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm.session import Session
from sqlalchemy.orm import aliased

url = 'sqlite+pysqlite:///../src/tests/resources/dbnav-c.sqlite'

engine = create_engine(url)
c = engine.connect()
meta = MetaData()
meta.reflect(bind=engine)

Article = aliased(meta.tables['article'], name='article1')
User = aliased(meta.tables['user'], name='user1')

session = Session(engine)
query = session.query(Article, User).join(User).filter(Article.columns['id'] == 1)

print query
print query.all()
