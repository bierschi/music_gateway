#!/usr/bin/env python3

from src.player.load_mpd import LoadMPD
from src.player.connect_mpd import ConnectMPD
from src.communication.mqtt import MQTT
from src.communication.scan_serial import ScanSerial
from src.communication.gps import GPS
from src.communication.internet_connection import InternetConnection

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

    # scan for available gps devices
    gps_port = ScanSerial().get_gps_port()
    if gps_port is not None:
        gps = GPS(gps_port, nmea_type='GPGGA')

    # create the MQTT instance to connect to remote broker
    # mqtt = MQTT(host="mqtt.swifitch.cz", port=1883)
    mqtt = MQTT(host=json_data['MQTT']['host'], port=int(json_data['MQTT']['port']),
                username=json_data['MQTT']['username'], password=json_data['MQTT']['password'])

    mqtt.add_topics(publish_topics=[{"topic_name": json_data['TOPIC_NAME']['topic'] + "/pub/database", "qos": 0},
                                    {"topic_name": json_data['TOPIC_NAME']['topic'] + "/pub/playback", "qos": 0},
                                    {"topic_name": json_data['TOPIC_NAME']['topic'] + "/pub/gps"     , "qos": 0}],

                    subscribe_topics=[{"topic_name": json_data['TOPIC_NAME']['topic'] + "/sub/song_control", "qos": 1}])

    # init of the background mqtt daemon thread
    mqtt.run()

    # create the MPD instance to localhost
    mpdclient = ConnectMPD("localhost", 6600)
    # query all songs in database
    mqtt.publish_msgs(mpdclient.get_all_songs_in_db(), topic_name=[json_data['TOPIC_NAME']['topic'] + '/pub/database'])

    while True:

        song_playlist = mpdclient.get_current_song_playlist()
        player_status = mpdclient.get_player_status()
        current_song = mpdclient.get_current_song()
        mqtt.publish_msgs({'current_song': current_song, 'song_playlist': song_playlist, 'player_status': player_status},
                          topic_name=[json_data['TOPIC_NAME']['topic'] + '/pub/playback'])
        if gps_port is not None:
            gps_data = gps.get_converted_data_dict()
            time_cet = gps_data['time_cet']
            longitude, latitude = gps_data['longitude'], gps_data['latitude']
            nmea_type, heigth_over_msl, number_of_sat = gps_data['nmea_type'], gps_data['height_over_msl'], gps_data['number_of_satellites']

            mqtt.publish_msgs({'gps_data': {'time': time_cet, 'longitude': longitude, 'latitude': latitude,
                                            'nmea_dataformat': nmea_type, 'height_over_msl': heigth_over_msl,
                                            'number_of_sat': number_of_sat}},
                              topic_name=[json_data['TOPIC_NAME']['topic'] + '/pub/gps'])
        else:
            sleep(1)


if __name__ == '__main__':
    music_gateway()
    #test()