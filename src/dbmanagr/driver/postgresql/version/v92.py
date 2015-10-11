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

STAT_ACTIVITY = """select
        sa.datname database_name,
        sa.pid pid,
        sa.usename username,
        coalesce(sa.client_addr || ':' || sa.client_port, '') as client,
        sa.xact_start transaction_start,
        sa.query_start query_start,
        sa.state state,
        regexp_replace(sa.query, '\s+', ' ', 'g') query,
        sa.waiting blocked,
        case
            when sa.waiting then string_agg(l.virtualxid, ',')
            else ''
        end blocked_by,
        now() - sa.xact_start as transaction_duration,
        now() - sa.query_start as query_duration
    from pg_stat_activity sa
        left join pg_locks l on l.pid = sa.pid
    where
        '{database}' in (sa.datname, '')
        and (
            sa.state in ({states})
            or array[{states}] = array['']
        )
        and (sa.state != 'disabled' or {disabled})
        and '{username}' in (sa.usename, '')
        and (
            sa.pid in ({pids})
            or array[{pids}] = array[-1]
        )
        and (
            '{pattern}' = ''
            or sa.query like '%{pattern}%'
        )
    group by 1, 2, 3, 4, 5, 6, 7, 8, 9
    order by sa.datname
"""
