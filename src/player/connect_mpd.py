import threading

from mpd import MPDClient
from time import sleep


class ConnectMPD:

    def __init__(self, host, port=None):
        """
        creates a MPD client instance

        :param host: hostname for the MPD server
        :param port: port to communicate with the MPD server
        """
        if isinstance(host, str):
            self.host = host
        else:
            raise TypeError("'host' must be Type of String")

        if port is None:
            self.port = 6600
        else:
            if isinstance(port, int):
                self.port = port
            else:
                raise TypeError('port must be Type of Int')

        self.client = MPDClient()
        self.client.connect(host, port)

        self.connected = True
        self.__thread = None
        self.__running = False
        self.start()

    def __del__(self):
        """
        Destructor
        """
        self.stop_thread()
        self.connected = False
        self.client.close()
        self.client.disconnect()

    def stop_thread(self):
        """
        method to stop the thread
        """
        if self.__thread is not None:
            self.__running = False
            self.__thread.join()
            self.__thread = None

    def start(self, as_daemon=None):
        """
        method to start the __run thread

        as_daemon: boolean attribute to run the thread as daemon or not
        """
        if self.__thread is None:
            self.__running = True
            self.__thread = threading.Thread(target=self.__run)
            # default behavior run thread as daemon
            if as_daemon is None:
                self.__thread.daemon = True
            else:
                if not isinstance(as_daemon, bool):
                    raise TypeError("'as_daemon' must be a boolean type")
                else:
                    self.__thread.daemon = as_daemon
            self.__thread.start()

    def __run(self):
        """
        daemon thread to ping to the mpd client
        """
        while self.__running:
            self.client.ping()
            sleep(55)

    def update_database(self):
        """
        when changes in music folder were made, update the database
        """
        if not self.connected:
            raise ConnectionError("mpd client lost the connection")
        else:
            self.client.update()
            return True

    def create_music_playlist(self):
        """
        creates a music playlist for all songs in database
        """
        if not self.connected:
            raise ConnectionError("mpd client lost the connection")

        if self.clear_current_playlist():
            if self.update_database():
                music_list = self.client.listall()
                all_songs = list()
                for file in range(0, len(music_list)):
                    single_song = music_list[file].get("file")
                    self.client.add(single_song)
                    all_songs.append(single_song)
                return all_songs

    def add_artist_to_pl(self, artist, new_playlist=False):
        """
        Find artist in db and adds them to the current/new playlist

        :param artist: artist_string to add to playlist
        :param new_playlist: False as default, Yes, create new playlist
        :return: song_pos to play for, if selected artist in database
                 None, if selected artist not in database
        """
        if isinstance(artist, str):
            resp_artist = self.client.find("Artist", artist)
            if len(resp_artist) == 0:
                song_pos = self.advanced_search_in_db(artist)
                if song_pos is None:
                    return None
                else:
                    return song_pos
            else:
                if new_playlist is False:
                    song_pos = self.get_current_songpos()
                    #if song_pos is None:
                    #    song_pos = 0
                    self.client.findadd("Artist", artist)
                else:
                    self.clear_current_playlist()
                    self.client.findadd("Artist", artist)
                    song_pos = 0

                return song_pos
        else:
            raise TypeError("'artist' must be Type of String")

    def add_title_to_pl(self, title):
        """
        Add desired genre to playlist, if genre is in db available

        :param title: title_string to add to playlist
        :return: song_pos to play for, if selected title in database
                 None, if selected title not in database

        """
        if isinstance(title, str):
            resp_title = self.client.find("Title", title)
            if len(resp_title) == 0:
                song_pos = self.advanced_search_in_db(title)
                if song_pos is None:
                    return None
                else:
                    return song_pos
            else:
                song_pos = self.get_current_songpos()
                self.client.findadd("Title", title)
                return song_pos

        else:
            raise TypeError("'title must be Type of String")

    def add_genre_to_pl(self, genre, new_playlist=False):
        """
        Add desired genre to playlist, if genre is in db available

        :param genre: genre_string to add to playlist
        :param new_playlist: False as default, Yes, create new playlist
        :return: song_pos to play for, if selected genre in database
                 None, if selected genre not in database
        """
        if isinstance(genre, str):
            resp_genre = self.client.find("Genre", genre)
            if len(resp_genre) == 0:
                song_pos = self.advanced_search_in_db(genre)
                if song_pos is None:
                    return None
                else:
                    return song_pos
            else:
                if new_playlist is False:
                    song_pos = self.get_current_songpos()
                    self.client.findadd("Genre", genre)
                else:
                    self.clear_current_playlist()
                    self.client.findadd("Genre", genre)
                    song_pos = 0
                return song_pos
        else:
            raise TypeError("'genre' must be Type of String")

    def advanced_search_in_db(self, search_str, search_type=None, s_pos=True):
        """
        search for specific string in database
        search_type can be any, Artist, Title, Genre..

        :param search_str: string to search in database
        :param search_type: string, "Any", "Artist", "Title", "Genre" ..
        :param s_pos: boolean, if True, it will be returned song_pos and db_response
                               if False, it will be returned only db_response
        :return: None, if no match were found
                 song_pos for the 'play method' to play the requested string
        """
        if not self.connected:
            raise ConnectionError("mpd client lost the connection")

        if isinstance(search_str, str):
            if search_type is None:
                db_response = self.client.search("Any", search_str)
                print(db_response)
            else:
                if isinstance(search_type, str):
                    db_response = self.client.search(search_type, search_str)
                else:
                    raise TypeError("'type' must be Type of String")
            if len(db_response) == 0:
                return None
            elif s_pos is False:
                return db_response
            else:
                song_pos = self.get_current_songpos()
                for resp in db_response:
                    print(resp.get('file'))
                    self.client.add(resp.get('file'))
                if song_pos is None:
                    song_pos = 0
                    return song_pos
                else:
                    return song_pos
        else:
            raise TypeError("'search_str' must be Type of String")

# QUERYING USEFUL INFORMATION

    def get_all_songs_in_db(self):
        """
        method to get all songs in database

        :return: list containing all songs from database

        ['Axwell _ Ingrosso - On My Way[audio].mp3', 'Axwell Λ Ingrosso - Dreamer (Official Video) feat. Trevor Guthrie.mp3', ]
        """
        if not self.connected:
            raise ConnectionError("mpd client lost the connection")

        return [files['file'] for files in self.client.listall()]

    def get_all_songinfos_from_db(self):
        """
        method to get detailed song infos for all songs in database

        :return: list containing dictionaries with the detailed song infos

        [{'last-modified': '2018-01-21T17:50:15Z', 'title': 'On My Way[audio]', 'time': '261',
          'file': 'Axwell _ Ingrosso - On My Way[audio].mp3', 'artist': 'Axwell /\\ Ingrosso', 'duration': '260.624'},
         {'last-modified': '2018-02-01T17:41:19Z', 'title': 'Dreamer (Official Video) feat. Trevor Guthrie', 'time': '234',
          'file': 'Axwell Λ Ingrosso - Dreamer (Official Video) feat. Trevor Guthrie.mp3', 'artist': 'Axwell Λ Ingrosso', 'duration': '234.371'}]
        """
        if not self.connected:
            raise ConnectionError("mpd client lost the connection")

        return self.client.listallinfo()

    def get_current_song(self):
        """
        displays the song info of the current song

        :return: dictionary with song info (id, artist, title, time, pos, duration file) of current song

        {'last-modified': '2018-02-27T12:25:10Z', 'title': 'Leave a Light On', 'file': 'Tom Walker - Leave a Light On.mp3',
         'id': '3', 'time': '186', 'artist': 'Tom Walker', 'pos': '1', 'duration': '186.201'}
        """
        if not self.connected:
            raise ConnectionError("mpd client lost the connection")

        return self.client.currentsong()

    def get_current_song_playlist(self):
        """
        displays the current playlist

        :return: list with all songs in current playlist

        ['The Chainsmokers - Sick Boy.mp3', 'Tom Walker - Leave a Light On.mp3']
        """
        if not self.connected:
            raise ConnectionError("mpd client lost the connection")

        return [song['file'] for song in self.client.playlistinfo()]

    def get_playlist_info(self):
        """
        detailed song infos from the current playlist

        :return: list containing dictionaries with the detailed song infos

        [{'last-modified': '2018-02-17T13:02:16Z', 'title': 'Sick Boy', 'file': 'The Chainsmokers - Sick Boy.mp3',
          'id': '2', 'time': '218', 'artist': 'The Chainsmokers', 'pos': '0', 'duration': '218.488'},
         {'last-modified': '2018-02-27T12:25:10Z', 'title': 'Leave a Light On', 'file': 'Tom Walker - Leave a Light On.mp3',
          'id': '3', 'time': '186', 'artist': 'Tom Walker', 'pos': '1', 'duration': '186.201'}]
        """
        return self.client.playlistinfo()

    def get_player_status(self):
        """
        reports the current status of the player and the volume level

        :return: dictionary containing status of player

        {'playlistlength': '2', 'random': '0', 'songid': '3', 'single': '0', 'volume': '-1', 'song': '1',
         'mixrampdb': '0.000000', 'playlist': '9', 'state': 'stop', 'consume': '0', 'repeat': '0'}
        """
        if not self.connected:
            raise ConnectionError("mpd client lost the connection")

        return self.client.status()

    def get_tagtypes(self):
        """
        get the available tagtypes from the mpd server

        :return: list containing available tagtypes
                 ['Artist', 'Album', 'Title', 'Track', 'Name', 'Genre', 'Date', 'Composer', 'Performer', 'Disc']
        """
        if not self.connected:
            raise ConnectionError("mpd client lost the connection")

        return self.client.tagtypes()

    def get_current_songpos(self):
        """
        method to get the current 'songpos', for selecting desired song in playlist

        :return: int number for the current songpos in playlist
        """
        if not self.connected:
            raise ConnectionError("mpd client lost the connection")

        pos_list = [pos.get('pos') for pos in self.client.playlistid()]
        pos_list = [int(pos) for pos in pos_list]
        if len(pos_list) > 0:
            return int(max(pos_list)) + 1
        else:
            return 0

    def get_all_artists_in_db(self):
        """
        method to get all artists in database

        :return: list, that contains all artists from database
        """

        return [artist.get('artist') for artist in self.client.listallinfo() if artist.get('artist') is not None]

    def get_all_titles_in_db(self):
        """
        method to get all titles in database

        :return: list, that contains all titles from database
        """
        return [title.get('title') for title in self.client.listallinfo() if title.get('title') is not None]

    def get_all_genres_in_db(self):
        """
        method to get all genres in database

        :return: list, that contains all genres from database
        """
        return [genre.get('genre') for genre in self.client.listallinfo() if genre.get('genre') is not None]


# CURRENT PLAYLIST

    def add_song_to_playlist(self, song):
        """
        add 'song' to current playlist

        :param song: song string
        """
        if isinstance(song, str):
            self.client.add(song)
        else:
            raise TypeError("song must be type of string")

    def clear_current_playlist(self):
        """
        clears current playlist
        """
        if not self.connected:
            raise ConnectionError("mpd client lost the connection")
        else:
            self.client.clear()
            return True

    def delete_song(self, songid=None):
        """
        deletes a song from the playlist

        :param songid: deletes song with "songid"
        """
        if not self.connected:
            raise ConnectionError("mpd client lost the connection")

        if songid is None:
            self.client.delete()
        else:
            self.client.deleteid(songid)

# PLAYBACK OPTIONS

    def set_random(self):
        """
        sets random state ON or OFF
        """
        if not self.connected:
            raise ConnectionError("mpd client lost the connection")

        state = self.get_player_status()
        random_state = state.get('random')

        if random_state == '0':
            self.client.random(1)
        else:
            self.client.random(0)

    def set_repeat(self):
        """
        sets repeat state ON or OFF
        """
        if not self.connected:
            raise ConnectionError("mpd client lost the connection")

        state = self.get_player_status()
        repeat_state = state.get('repeat')

        if repeat_state == '0':
            self.client.repeat(1)
        else:
            self.client.repeat(0)

# CONTROLLING PLAYBACK

    def pause(self):
        """
        toggles pause/ resume playing
        """
        if not self.connected:
            raise ConnectionError("mpd client lost the connection")

        states = self.get_player_status()
        player_state = states.get('state')

        if player_state == 'play':
            self.client.pause(1)
        elif player_state == 'pause':
            self.client.pause(0)
        else:
            print("state: stop is active")

    def shuffle(self):
        """
        shuffles the current playlist
        """
        if not self.connected:
            raise ConnectionError("mpd client lost the connection")
        else:
            self.client.shuffle()

    def play(self, songpos=None):
        """
        starts playing
        """
        if not self.connected:
            raise ConnectionError("mpd client lost the connection")

        if songpos is None:
            self.client.play()
        else:
            self.client.play(songpos)

    def stop(self):
        """
        stops playing
        """
        if not self.connected:
            raise ConnectionError("mpd client lost the connection")
        else:
            self.client.stop()

    def next(self):
        """
        plays next song in the playlist
        """

        if not self.connected:
            raise ConnectionError("mpd client lost the connection")
        else:
            states = self.get_player_status()
            player_state = states.get('state')
            if player_state == 'play' or player_state == 'pause':
                self.client.next()
            else:
                print("not playing")

    def previous(self):
        """
        plays previous song in the playlist
        """
        if not self.connected:
            raise ConnectionError("mpd client lost the connection")
        else:
            states = self.get_player_status()
            player_state = states.get('state')
            if player_state == 'play' or player_state == 'pause':
                self.client.previous()
            else:
                print("not playing")

    def test(self):
        all_songs = self.get_all_songs_in_db()
        with open("Lieder.txt", 'w', encoding='utf-8') as file:
            for song in all_songs:
                file.writelines(song + "\n")


if __name__ == "__main__":
    print("test")
    mpdclient = ConnectMPD("localhost", 6600)
    #print(mpdclient.get_current_song_playlist())
    #print(mpdclient.get_all_songs_in_db())
    mpdclient.test()
    #mpdclient.stop()