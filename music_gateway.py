#!/usr/bin/env python3

from src.player.load_mpd import LoadMPD
from src.communication.mqtt import MQTT
from src.player.connect_mpd import ConnectMPD
from time import sleep


def music_gateway():
    # load the mpd server depending on the operating system
    LoadMPD()

    # create the MQTT intance to connect to remote broker
    mqtt = MQTT(host="mqtt.swifitch.cz", port=1883)
    mqtt.add_topics(publish_topics=[{"topic_name": "music_gateway/pub/song_playlist", "qos": 0},
                                    {"topic_name": "music_gateway/pub/player_status", "qos": 0},
                                    {"topic_name": "music_gateway/pub/current_song",  "qos": 0}],

                    subscribe_topics=[{"topic_name": "music_gateway/sub/song_control", "qos": 1},
                                      {"topic_name": "music_gateway/sub/",             "qos": 1}])

    # init of the background daemon thread
    mqtt.run()

    # create the MPD instance to localhost
    mpdclient = ConnectMPD("localhost", 6600)
    mpdclient.create_music_playlist()
    while True:
        song_playlist = mpdclient.get_current_song_playlist()
        player_status = mpdclient.get_player_status()
        current_song = mpdclient.get_current_song()
        mqtt.publish_msgs(song_playlist, topic_name=['music_gateway/pub/song_playlist'])
        mqtt.publish_msgs(player_status, topic_name=['music_gateway/pub/player_status'])
        mqtt.publish_msgs(current_song,  topic_name=['music_gateway/pub/current_song'])
        sleep(1)


if __name__ == '__main__':
    music_gateway()
