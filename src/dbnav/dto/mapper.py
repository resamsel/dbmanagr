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

from dbnav.dto.row import Row
from dbnav.dto.column import Column
from dbnav.dto.foreignkey import ForeignKey
from dbnav.dto.table import Table


def to_dto(model):
    if type(model) is dict:
        return dict(map(lambda (k, v): (k, to_dto(v)), model.iteritems()))
    if type(model) is list:
        return map(to_dto, model)
    if model.__class__.__name__ == 'Row':
        return Row(to_dto(model.table), to_dto(model.row))
    if model.__class__.__name__ == 'Column':
        return Column(
            name=model.name,
            tablename=model.table.name,
            type=model.type,
            primary_key=model.primary_key
        )
    if model.__class__.__name__ == 'ForeignKey':
        return ForeignKey(a=to_dto(model.a), b=to_dto(model.b))
    if model.__class__.__name__ == 'Table':
        return Table(
            name=model.name,
            uri=model.uri,
            owner=model.owner,
            size=model.size,
            primary_key=model.primary_key,
            columns=to_dto(model.columns()),
            foreign_keys=to_dto(model.foreign_keys())
        )
    return model
