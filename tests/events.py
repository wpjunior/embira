import unittest
from embira import EventHandler, signal

class EventTest(unittest.TestCase):
    
    def setUp(self):
        class Events(EventHandler):
            pass

        self.Events = Events
    
    def test_signal_connect(self):
        
        ev = self.Events()
        self.assertEqual(ev._listeners, {})

        @ev.on('msgReceived')
        def msg_received(*args):
            pass

        self.assertEqual(ev._listeners, {'msgReceived': [msg_received]})


        def one_signal(*args):
            pass

        ev.on('manage', one_signal)
        self.assertEqual(ev._listeners, {'msgReceived': [msg_received],
                                         'manage': [one_signal]})

    def test_signal_disconnect(self):

        ev = self.Events()

        @ev.on('attention')
        def msg_received(*args):
            pass

        ev.off()
        self.assertEqual(ev._listeners, {})

        @ev.on('attention2')
        def msg_received2(*args):
            pass
        
        @ev.on('attention3')
        def msg_received3(*args):
            pass

        ev.off('attention2')
        self.assertEqual(ev._listeners, {'attention3': [msg_received3]})

    def test_trigger_signal(self):
        ev = self.Events()
        self.assertEqual(ev._listeners, {})
        self.called = False

        @ev.on('callMe')
        def call_me(*args):
            self.called = True

        ev.trigger('callMe')

        self.assertTrue(self.called)
        del self.called

        self.count = 0

        def inc(*args):
            self.count += 1

        for i in xrange(5):
            ev.on('inc', inc)

        ev.trigger('inc')
        self.assertEqual(self.count, 5)

    def test_trigger_signal_args(self):
        ev = self.Events()

        self.assertEqual(ev._listeners, {})

        @ev.on('callMe')
        def call_me(*args, **kwargs):
            self.assertEqual(args, ('wilson',))
            self.assertEqual(kwargs, {'ativ': "Programmer",
                                      'music': "Heavy Metal"})

            return "OK"

        self.assertEqual(ev._listeners['callMe'], [call_me])

        resp = ev.trigger('callMe', 'wilson',
                          ativ="Programmer",
                          music="Heavy Metal")

        self.assertEqual(resp, "OK")
        

    def test_class_event(self):
        class MyEvents(EventHandler):
            @signal('wilson')
            def teste(*args):
                pass

        self.assertEqual(len(MyEvents._pre_signals), 1)
        ev = MyEvents()
