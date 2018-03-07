from src.player.control_mpd import ControlMPD, FindInDatabase
from src.player.connect_mpd import ConnectMPD

import json
import logging as log
from time import sleep

try:
    import paho.mqtt.client as mqtt
except ImportError as e:
    print(str(e))


class MQTT(mqtt.Client):
    """
    MQTT class to create a mqtt instance to publish and subscribe messages
    """

    def __init__(self, host, port=None, username=None, password=None):
        """

        :param host: hostname of the broker
        :param port: network port to server host, Default: 1883
        :param username: username for the broker authentication
        :param password: password for the broker authentication
        """
        super().__init__(client_id="")  # TODO RANDOM
        self.host = host

        try:
            self.client = mqtt.Client()
        except ConnectionError as e:
            print(str(e))
            self.client = None

        if port is None:
            self.port = 1883
        else:
            if isinstance(port, int):
                self.port = port
            else:
                raise TypeError("port must be an integer")

        if username is None:
            self._username = username
            self._password = password
        else:
            if isinstance(username, str):
                self._username = username
                self._password = password
                # Set a username and optionally a password for broker authentication. Must be called before connect()
                self.client.username_pw_set(self._username, self._password)
            else:
                raise TypeError("username must be a string object")

        self.pub_topics = list()
        self.sub_topics = list()

        # callback methods initialization
        self.client.on_connect = self.on_connect
        self.client.on_disconnect = self.on_disconnect
        self.client.on_message = self.on_message
        self.client.on_publish = self.on_publish
        self.client.on_subscribe = self.on_subscribe
        self.client.on_unsubscribe = self.on_unsubscribe
        # create mpdclient
        self.mpdclient = ConnectMPD("localhost", 6600)

    def __del__(self):
        """
        Destructor
        """
        if self.client is not None:
            # Call loop_stop() to stop the background thread
            self.client.loop_stop()
            # Disconnect from the broker cleanly
            self.client.disconnect()

    def run(self):
        """
        run method for connecting to the remote broker and starting the loop thread

        The connect() function connects the client to a broker. This is a blocking function.
        Calling loop_start() once, before or after connect*(), runs a thread in the background to call loop()
        automatically. This frees up the main thread for other work that may be blocking.
        This call also handles reconnecting to the broker!

        Throws ConnectionError or TimeoutError if no connection has established to the remote broker
        """
        if self.client is not None:
            try:
                log.info("connect to broker")
                self.client.connect(self.host, self.port)
            except (ConnectionError, TimeoutError) as e:
                print(str(e))

            self.client.loop_start()

    def reconnect(self):
        """
        method to reconnect to the broker
        """
        if self.client is not None:
            self.client.reconnect()
        else:
            raise ConnectionError("please check the client connection")

    def add_topics(self, **kwargs):
        """
        method to add the desired publish and subscribe topics into a list container

        :param publish_topics=[{"topic_name": "publish_test", "qos": 0}, {"topic_name": "publish_test2", "qos": 2}]
        :param subscribe_topics=[{"topic_name": "subscribe_test", "qos": 0}, {"topic_name": "subscribe_test2", "qos": 1}]

        """
        if 'publish_topics' in kwargs and len(kwargs['publish_topics']) > 0:
            log.info("add pub_topics")
            for pub_topic in kwargs['publish_topics']:
                if pub_topic.get('qos') < 0 or pub_topic.get('qos') > 2:
                    pub_topic.update({'topic_name': pub_topic.get('topic_name'), 'qos': 0})
            if len(self.pub_topics) == 0:
                self.pub_topics = kwargs['publish_topics']
            else:
                for pub_topic in kwargs['publish_topics']:
                    self.pub_topics.append(pub_topic)

        if 'subscribe_topics' in kwargs and len(kwargs['subscribe_topics']) > 0:
            log.info("add sub_topics")
            for sub_topic in kwargs['subscribe_topics']:
                if sub_topic.get('qos') < 0 or sub_topic.get('qos') > 2:
                    sub_topic.update({'topic_name': sub_topic.get('topic_name'), 'qos': 0})
            if len(self.sub_topics) == 0:
                self.sub_topics = kwargs['subscribe_topics']
            else:
                for sub_topic in kwargs['subscribe_topics']:
                    self.sub_topics.append(sub_topic)

    def delete_topics(self, topics=None):
        """
        method to delete desired publish or subscribe topics, if 'topics' is None all publish and subscribe
        topics will be deleted

        :param topics: list which contain the topics to delete, topics=['test'] # only topic 'test' will be deleted

        """
        if topics is None:
            log.info("delete all topics")
            self.pub_topics.clear()
            self.sub_topics.clear()
        else:
            if isinstance(topics, list) and len(topics) > 0:
                log.info("delete only selected topics")
                for i in range(0, len(topics)):
                    for pub in self.pub_topics:
                        if pub.get('topic_name') == topics[i]:
                            self.pub_topics.remove(pub)
                    for sub in self.sub_topics:
                        if sub.get('topic_name') == topics[i]:
                            self.sub_topics.remove(sub)
            else:
                raise TypeError("'topics must be a list")

    def __subscribe_topics(self):
        """
        method to subscribe topics to the remote broker, is called in on_connect callback

        """
        if len(self.sub_topics) > 0:
            log.info("subscribe topics")
            sub_topics = list()
            for sub in self.sub_topics:
                sub_tuple = sub.get('topic_name'), sub.get('qos')
                sub_topics.append(sub_tuple)
            self.client.subscribe(sub_topics)

    def unsubscribe_topics(self, topics=None):
        """
        method to unsubscribe topics

        :param topics: list which contain the topics to unsubscribe

        unsubscribe_topics(topics=["subscribe_test"]) # topic 'subscribe_test' will be unsubscribed

        """
        if topics is None:
            log.info("unsubscribe all sub_topics")
            unsub_list = list()
            for sub in self.sub_topics:
                unsub_list.append(sub.get('topic_name'))
            self.client.unsubscribe(unsub_list)
        else:
            if isinstance(topics, list):
                log.info("unsubscribe selected sub_topics")
                self.client.unsubscribe(topics)

    def get_sub_topics(self):
        """
        method to get the subscribe topics

        :return self.sub_topics: list which contain the subscribe topics
                           None: if length of self.sub_topics is 0
        """
        if len(self.sub_topics) > 0:
            return self.sub_topics
        else:
            return None

    def get_pub_topics(self):
        """
        method to get the publish topics

        :return self.pub_topics: list which contain the publish topics
                           None: if length of self.pub_topics is 0
        """
        if len(self.pub_topics) > 0:
            return self.pub_topics
        else:
            return None

    def publish_msgs(self, msg, topic_name=None):
        """

        :param msg:
        :param topic_name: list which contain the topic names to publish the messages

        publish_msgs("msg_bsp")                  # msg will be sent to all publish topics, predefined in 'add_topic'
        publish_msgs("msg", topic_name=['test']) # msg will be sent only to topic 'test'

        """
        # build a valid json_string
        try:
            log.info("create json string")
            json_string = self.__create_json_string(msg)
        except TypeError as e:
            print(str(e))
            return None

        pub_topics = self.get_pub_topics()
        if topic_name is None:
            log.info("send msg to all pub_topics")
            if pub_topics is not None:
                for pub_topic in pub_topics:
                    self.client.publish(pub_topic.get('topic_name'), json_string)
            else:
                raise ValueError("No topics for publishing were selected")
        else:
            if isinstance(topic_name, list):
                log.info("send msg to selected pub_topics")
                for i in range(0, len(topic_name)):
                    if pub_topics is not None:
                        for pub_topic in pub_topics:
                            if topic_name[i] in pub_topic.get('topic_name'):
                                print(json_string)
                                self.client.publish(topic=pub_topic.get('topic_name'),
                                                    payload=json_string,
                                                    qos=pub_topic.get('qos'))
            else:
                raise TypeError("'topic_name must be a list")

    def __create_json_string(self, msg):
        """
        method to create a valid json string

        :return valid json string
        """
        return json.dumps(msg)

    def subscribe_msgs(self, topic, msg):
        """

        :return:
        """
        log.info("topic:{}, msg: {}".format(topic, msg))

        if topic == 'music_gateway/sub/song_control':
            ControlMPD(self, self.mpdclient, json.loads(msg))

        if topic == 'music_gateway/sub/find_song':
            FindInDatabase(self.mpdclient, json.loads(msg))

# CALLBACKS

    def on_connect(self, client, userdata, flags, rc):
        """
        called when the broker responds to our connection request

        :param client: the client instance for this callback
        :param userdata: the private user data as set in Client() or userdata_set()
        :param flags: response flags sent by the broker
        :param rc: the connection result
        """
        print("Connected to the remote broker")

        # subscribing in on_connect() means if we lose the connection and reconnect then subscription will be renewed.
        self.__subscribe_topics()

    def on_disconnect(self, client, userdata, rc):
        """
        called when the client disconnects from the broker

        :param client: the client instance for this callback
        :param userdata: the private user data as set in Client() or userdata_set()
        :param rc: the disconnection result
        """
        print("Disconnected from the remote broker")

    def on_message(self, client, userdata, msg):
        """
        called when a message has been received on a topic that the client subscribes to. This callback will be called
        for every message received.

        :param client: the client instance for this callback
        :param userdata: the private user data as set in Client() or userdata_set()
        :param msg: an instance of MQTTMessage. This is a class with memebers topic, payload, qos, retain
        """
        print("On_message callback")
        self.subscribe_msgs(msg.topic, str(msg.payload, 'utf-8'))

    def on_publish(self, client, userdata, mid):
        """
        called when a message that was to be sent using the publish() call has completed transmission to the broker.

        :param client: the client instance for this callback
        :param userdata: the private user data as set in Client() or userdata_set()
        :param mid: The mid variable matches the mid variable returned from the corresponding publish() call,
        to allow outgoing messages to be tracked
        """
        print("On_publish callback")

    def on_subscribe(self, client, userdata, mid, granted_qos):
        """
        called when the broker responds to a subscribe request

        :param client: client: the client instance for this callback
        :param userdata: the private user data as set in Client() or userdata_set()
        :param mid: the mid variable matches the mid variable returned from the corresponding subscribe() call
        :param granted_qos: The granted_qos variable is a list of integers that give the QoS level the broker has
        granted for each of the different subscription requests
        """
        print("Remote broker responds the subscribe request")

    def on_unsubscribe(self, client, userdata, mid):
        """
        called when the broker responds to an unsubscribe request. The mid variable matches the mid variable returned
        from the corresponding unsubscribe() call.
        :param client: the client instance for this callback
        :param userdata: the private user data as set in Client() or userdata_set()
        :param mid: matches the mid variable returned from the corresponding unsubscribe() call
        """
        print("Unsubscribe topic")


if __name__ == '__main__':
    mqtt = MQTT(host="mqtt.swifitch.cz", port=1883)
    mqtt.add_topics(publish_topics=[{"topic_name": "test", "qos": 0}, {"topic_name": "test2", "qos": 2}],
                    subscribe_topics=[{"topic_name": "sub_test", "qos": 0}, {"topic_name": "sub_test2", "qos": 1}])
    mqtt.run()
    mqtt.add_topics(publish_topics=[{"topic_name": "pub_bsp", "qos": 3}])
    print(mqtt.get_pub_topics())
    print(mqtt.get_sub_topics())

    while True:
        mqtt.publish_msgs(["hallo", "servus", {"abc": 3}], topic_name=['test2'])
        mqtt.publish_msgs("sec: topic", topic_name=['pub_bsp'])
        sleep(2)
