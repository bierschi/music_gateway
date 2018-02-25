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
    mpd.conf
    mpd.db
    mpd.exe
    mpd.log

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
    test_mpd_connection.py
    test_mqtt.py

LICENSE
music_gateway.py
README.md
setup.py
</pre></code>