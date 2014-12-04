#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright © 2014 René Samselnig
#
# This file is part of Database Navigator.
#
# Database Navigator is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Database Navigator is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Database Navigator.  If not, see <http://www.gnu.org/licenses/>.
#

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

for k, t in meta.tables.iteritems():
    for fk in t.foreign_keys:
        print '{t.name}: {fk.parent.table.name}.{fk.parent.key} -> {fk.column.table.name}.{fk.column.key}'.format(
            fk=fk, t=t)

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
