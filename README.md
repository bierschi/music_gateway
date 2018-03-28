# Music Gateway

A repository to control music over mobile network with the MQTT protocol

## Usage
clone this repository:

`git clone https://github.com/bierschi/music_gateway.git`

and:

`cd music_gateway`

install the project with `setup.py`:

`python3 setup.py install`

Windows (python version 3.5):

`py -3.5 setup.py install`

## Current Status / Testing

Download a mqtt client like MQTT.FX http://mqttfx.jensd.de/index.php/download

#### Subscribe following `publish_topics` to see all songs in database, the current playback state and gps data if a gps sensor is connected

publish_topics:
- `music_gateway/pub/database` <br>
- `music_gateway/pub/playback` <br>
- `music_gateway/pub/gps`
#### Publish the following actions on this topic:

subscribe_topics:
- `music_gateway/sub/song_control`

This commands are working:

<pre><code>
{"action": "play"}
{"action": "stop"}
{"action": "next"}
{"action": "previous"}
{"action": "pause"}
{"action": "shuffle"}
{"action": "clear_playlist"}
{"action": "random"}
{"action": "repeat"}
{"action": "update"}

{"desired_song": "Nano - Hold On(Official Audio).mp3"}
{"add_song": "Nano - Hold On(Official Audio).mp3"}
{"delete_song": "Nano - Hold On(Official Audio).mp3"}
</pre></code>

`add_song`: adds a song from the database into current playlist, song must available in `music_gateway/pub/database`

`desired_song`: select the desired song from the current playlist

`delete_song`: deletes a song from the current playlist

<br>

**commands will later be replaced by an APP!**

## Settings in file `configuration.json`

example settings for a public broker. `topic` can be any desired string

<pre><code>
{
  "MQTT": {
    "host"    : "mqtt.swifitch.cz",
    "port"    : "1883",
    "username": "",
    "password": ""
  },
  "TOPIC_NAME":{
    "topic"    : "music_gateway"
  }
}
</pre></code>

## Windows

## Linux

## MAC OS


## Electrical Circuit for Raspberry Pi



## Project Layout
<pre><code>
/music
    /radio_playlists
        .m3u files
    /songs
        folder_for_songs
    mpd.exe

/scripts
    music_gateway.sh

/src
    /communication
        gps.py
        gsm.py
        mqtt.py
        scan_serial.py
    /player
        connect_mpd.py
        control_mpd.py
        load_mpd.py

/test
    test_gps.py
    test_gsm.py
    test_mqtt.py
    test_connect_mpd.py
    test_control_mpd.py
    test_load_mpd.py

definitions.py
LICENSE
music_gateway.py
README.md
requirements.txt
setup.py
</pre></code>