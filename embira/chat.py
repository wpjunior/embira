#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  Copyright (C) 2011 Wilson Pinto Júnior <wilsonpjunior@gmail.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from embira import json_helper
from embira.events import EventHandler

class Chat(EventHandler):
    last_id = 0

    def _generate_new_msg(self, name, args=(), kwargs={}):
        data = {'name': name}

        self.last_id += 1
        data['_id'] = self.last_id
        
        if args:
            data['args'] = args
        
        if kwargs:
            data['kwargs'] = kwargs

        return json_helper.dumps(data)
        
    def send(self, name, *args, **kwargs):
        data = self._generate_new_msg(name, args, kwargs)
