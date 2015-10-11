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
        sa.procpid pid,
        sa.usename username,
        coalesce(sa.client_addr || ':' || sa.client_port, '') as client,
        sa.xact_start transaction_start,
        sa.query_start query_start,
        case
            when sa.current_query = '<IDLE>' then 'idle'
            when sa.current_query = '<IDLE> in transaction'
                then 'idle in transaction'
            when sa.current_query = '<insufficient privilege>' then 'disabled'
            when sa.current_query not like '<%>' then 'active'
            else '?'
        end state,
        regexp_replace(sa.current_query, '\s+', ' ', 'g') query,
        sa.waiting blocked,
        case
            when sa.waiting then string_agg(l.virtualxid, ',')
            else ''
        end blocked_by,
        now() - sa.xact_start as transaction_duration,
        now() - sa.query_start as query_duration
    from pg_stat_activity sa
        left join pg_locks l on l.pid = sa.procpid
    where
        '{database}' in (sa.datname, '')
        and (
            case
                when sa.current_query = '<IDLE>' then 'idle'
                when sa.current_query = '<IDLE> in transaction'
                    then 'idle in transaction'
                when sa.current_query = '<insufficient privilege>'
                    then 'disabled'
                when sa.current_query not like '<%>' then 'active'
                else '?'
            end in ({states})
            or array[{states}] = array['']
        )
        and (
            {disabled}
            or case
                when sa.current_query = '<IDLE>' then 'idle'
                when sa.current_query = '<IDLE> in transaction'
                    then 'idle in transaction'
                when sa.current_query = '<insufficient privilege>'
                    then 'disabled'
                when sa.current_query not like '<%>' then 'active'
                else '?'
            end != 'disabled'
        )
        and '{username}' in (sa.usename, '')
        and (
            sa.procpid in ({pids})
            or array[{pids}] = array[-1]
        )
        and (
            '{pattern}' = ''
            or sa.current_query like '%{pattern}%'
        )
    group by 1, 2, 3, 4, 5, 6, 7, 8, 9
    order by sa.datname
"""
