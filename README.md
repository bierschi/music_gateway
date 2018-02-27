# Music Gateway

A repository to control music over mobile network with the MQTT protocol




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

LICENSE
music_gateway.py
README.md
setup.py
</pre></code>