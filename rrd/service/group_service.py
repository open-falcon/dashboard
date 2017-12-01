# -*- coding:utf-8 -*-
# Copyright 2017 Xiaomi, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


__author__ = 'Ulric Qin'
from rrd.store import db
from rrd.model.portal.host_group import HostGroup

from rrd.utils.logger import logging
log = logging.getLogger(__file__)

def delete_group(group_id=None):
    try:
        cursor = db.execute('delete from grp where id = %s', [group_id])
        db.execute('delete from grp_host where grp_id = %s', [group_id], cursor=cursor)
        db.execute('delete from grp_tpl where grp_id = %s', [group_id], cursor=cursor)
        db.execute('delete from plugin_dir where grp_id = %s', [group_id], cursor=cursor)
        db.commit()
        return ''
    except Exception, e:
        log.error(e)
        db.rollback()
        return 'delete group %s fail' % group_id
    finally:
        cursor and cursor.close()


def rename(old_str=None, new_str=None, login_user=None):
    print(old_str, new_str, login_user)
    gs = HostGroup.select_vs(where='create_user = %s and come_from = %s', params=[login_user, 1])
    for g in gs:
        HostGroup.update_dict({'grp_name': g.grp_name.replace(old_str, new_str)}, 'id=%s', [g.id])
    return ''

