import unittest
from embira.chat import Chat
from embira import json_helper

class ChatTest(unittest.TestCase):
    def test_send_msg(self):
        class MyChat(Chat):
            pass

        m = MyChat()

        data = m._generate_new_msg('msg', ['a', 'b'],
                                   {'name': "wilson",
                                    'typ': "alegre"})

        dump_data = json_helper.loads(data)

        self.assertEqual(dump_data['_id'], 1)
