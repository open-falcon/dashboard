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
from .bean import Bean


class PluginDir(Bean):
    _tbl = 'plugin_dir'
    _id = 'id'
    _cols = 'id, grp_id, dir, create_user'

    def __init__(self, _id, grp_id, plugin_dir, create_user):
        self.id = _id
        self.grp_id = grp_id
        self.dir = plugin_dir
        self.create_user = create_user

