# Music Gateway



## Electrical Circuit



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
        mpd_connection.py

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