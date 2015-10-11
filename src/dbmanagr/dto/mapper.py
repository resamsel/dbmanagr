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

import logging

from dbmanagr.dto.row import Row
from dbmanagr.dto.column import Column
from dbmanagr.dto.foreignkey import ForeignKey
from dbmanagr.dto.table import Table
from dbmanagr.dto.node import ColumnNode, ForeignKeyNode, TableNode, NameNode

logger = logging.getLogger(__name__)


def to_dto(model):
    if type(model) is dict:
        return dict(map(lambda (k, v): (k, to_dto(v)), model.iteritems()))
    if type(model) in (tuple, list, set):
        return map(to_dto, model)
    if model.__class__.__name__ == 'Row':
        return Row(
            table=to_dto(model.table),
            row=to_dto(model.row),
            autocomplete=model.autocomplete()
        )
    if model.__class__.__name__ == 'Column':
        return Column(
            name=model.name,
            tablename=model.table.name,
            type_=model.type,
            nullable=model.nullable,
            default=model.default,
            autoincrement=model.autoincrement,
            primary_key=model.primary_key,
            autocomplete=model.autocomplete()
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
            foreign_keys=to_dto(model.foreign_keys()),
            autocomplete=model.autocomplete()
        )
    if model.__class__.__name__ == 'ColumnNode':
        return ColumnNode(to_dto(model.column), model.indent)
    if model.__class__.__name__ == 'ForeignKeyNode':
        return ForeignKeyNode(
            to_dto(model.fk), to_dto(model.parent), model.indent)
    if model.__class__.__name__ == 'TableNode':
        return TableNode(to_dto(model.table), model.indent)
    if model.__class__.__name__ == 'NameNode':
        return NameNode(to_dto(model.name), model.indent)
    return model
