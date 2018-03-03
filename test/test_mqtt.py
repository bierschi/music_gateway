import unittest
from src.communication.mqtt import MQTT


class TestMQTT(unittest.TestCase):

    def setUp(self):
        self.mqtt = MQTT(host="mqtt.swifitch.cz", port=1883)

    def test_add_topics(self):
        pass

    def test_delete_topics(self):
        pass

    def test_unsubscribe_topics(self):
        pass

    def test_get_sub_topics(self):
        pass

    def test_get_pub_topics(self):
        pass

    def test_publish_msgs(self):
        pass

    def test_subscribe_msgs(self):
        pass

    def tearDown(self):
        self.mqtt.__del__()


if __name__ == '__main__':
    unittest.main()