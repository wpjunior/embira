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

class EventNotFound(Exception): pass

class EventHandlerType(type):
    def __new__(cls, name, bases, attrs):
        metaclass = attrs.get('__metaclass__')
        super_new = super(EventHandlerType, cls).__new__
        if metaclass and issubclass(metaclass, EventHandlerType):
            return super_new(cls, name, bases, attrs)

        
        pre_signals = {}

        for k, v in attrs.iteritems():
            if not isinstance(v, ConstructorSignal):
                continue
           
            if not pre_signals.has_key(v.name):
                pre_signals[v.name] = []

            pre_signals[v.name].append(v.func.__name__)
            attrs[k] = v.func

        attrs['_pre_signals'] = pre_signals
        new_class = super_new(cls, name, bases, attrs)
        return new_class

class EventHandler(object):
    __metaclass__ = EventHandlerType

    def __init__(self):
        self._listeners = {}

        if self.__class__._pre_signals:
            for name, sigs in self.__class__._pre_signals.iteritems():
                for sig in sigs:
                    self.on(name,
                            getattr(self, sig))

    def on(self, name, func=None):
        """
        Register a event
        @name: name of event
        """
            
        def register(f):
            if not self._listeners.has_key(name):
                self._listeners[name] = []

            self._listeners[name].append(f)
            return f

        if func:
            return register(func) # method

        return register #decorator method

    def off(self, name=None):
        """
        Disconnect all event handlers
        @name: name of event if None clean all signals
        """
        if not name:
            self._listeners = {}
            return

        if self._listeners.has_key(name):
            del self._listeners[name]

    def trigger(self, name, *args, **kwargs):
        """
        Emit a event
        name of event
        """
        if not self._listeners.has_key(name):
            raise EventNotFound

        results = []

        for func in self._listeners[name]:
            try:
                resp = func(*args, **kwargs)
                results.append(resp)
            except Exception, e:
                results.append(e)

        if len(results) == 1:
            return results[0]
        return results

class ConstructorSignal(object):
    def __init__(self, name, func):
        self.name = name
        self.func = func

def signal(name):
    def decorator(f):
        return ConstructorSignal(name, f)
    return decorator
