
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

            pre_signals[v.name].append(v.func)
            attrs[k] = v.func

        attrs['_pre_signals'] = pre_signals
        new_class = super_new(cls, name, bases, attrs)
        return new_class

class EventHandler(object):
    __metaclass__ = EventHandlerType

    def __init__(self):
        self._listeners = {}

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
