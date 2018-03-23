#!/usr/bin/env python3

from src.player.load_mpd import LoadMPD
from src.communication.mqtt import MQTT
from src.player.connect_mpd import ConnectMPD

from time import sleep
import logging as log
import json

verbose = True

if verbose:
    log.basicConfig(format="%(asctime)s - %(levelname)s: %(message)s", level=log.DEBUG)
else:
    log.basicConfig(format="%(levelname)s: %(message)s")


def test():
    LoadMPD()


def music_gateway():
    # load the mpd server depending on the operating system
    LoadMPD()

    # load all settings in configuration.json
    with open('configs/configuration.json') as json_file:
        json_data = json.load(json_file)

    # create the MQTT instance to connect to remote broker
    # mqtt = MQTT(host="mqtt.swifitch.cz", port=1883)
    mqtt = MQTT(host=json_data['MQTT']['host'], port=int(json_data['MQTT']['port']),
                username=json_data['MQTT']['username'], password=json_data['MQTT']['password'])

    mqtt.add_topics(publish_topics=[{"topic_name": "music_gateway/pub/database", "qos": 0},
                                    {"topic_name": "music_gateway/pub/playback", "qos": 0},
                                    {"topic_name": "music_gateway/pub/gps"     , "qos": 0}],

                    subscribe_topics=[{"topic_name": "music_gateway/sub/song_control", "qos": 1}])

    # init of the background mqtt daemon thread
    mqtt.run()

    # create the MPD instance to localhost
    mpdclient = ConnectMPD("localhost", 6600)
    # query all songs in database
    mqtt.publish_msgs(mpdclient.get_all_songs_in_db(), topic_name=['music_gateway/pub/database'])

    #mpdclient.create_music_playlist()
    #mpdclient.clear_current_playlist()

    while True:
        song_playlist = mpdclient.get_current_song_playlist()
        player_status = mpdclient.get_player_status()
        current_song = mpdclient.get_current_song()
        mqtt.publish_msgs({'current_song': current_song, 'song_playlist': song_playlist, 'player_status': player_status},
                          topic_name=['music_gateway/pub/playback'])
        sleep(1)


if __name__ == '__main__':
    music_gateway()
    #test()