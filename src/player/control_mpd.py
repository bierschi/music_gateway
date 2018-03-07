

class ControlMPD():

    def __init__(self, mqtt_c, mpd_c, msg):
        """
        constructor to handle the mpd playback
        :param mpdclient: instance for the mpd
        :param msg: msg string like 'play', 'stop' ...
        """
        self.mqtt = mqtt_c
        self.mpdclient = mpd_c
        self.msg = msg

        if 'action' in self.msg.keys():
            if self.msg['action'] in {'play', 'stop', 'previous', 'pause', 'next', 'shuffle', 'clear_playlist'}:
                self.handle_playback(self.msg['action'])
            elif self.msg['action'] in {'random', 'repeat', 'clear', 'update'}:
                self.handle_playback_option(self.msg['action'])
        elif 'desired_song' in self.msg.keys():
            self.select_song_in_playlist(self.msg['desired_song'])

        elif 'add_song' in self.msg.keys():
            self.add_song_from_db(self.msg['add_song'])

        elif 'delete_song' in self.msg.keys():
            self.del_song_from_playlist(self.msg['delete_song'])

    def handle_playback(self, action):
        """
        method to handle simple playback option

        :param action: msg string like 'play', 'stop' ...
        """

        if action == 'play':
            self.mpdclient.play()
        elif action == 'stop':
            self.mpdclient.stop()
        elif action == 'next':
            self.mpdclient.next()
        elif action == 'pause':
            self.mpdclient.pause()
        elif action == 'previous':
            self.mpdclient.previous()
        elif action == 'shuffle':
            self.mpdclient.shuffle()
        elif action == 'clear_playlist':
            self.mpdclient.clear_current_playlist()

    def handle_playback_option(self, action):
        """
        method to handle advanced playback option

        :param action: msg string like 'random', 'repeat' ...
        """
        if action == 'random':
            self.mpdclient.set_random()
        elif action == 'repeat':
            self.mpdclient.set_repeat()
        elif action == 'clear':
            self.mpdclient.clear_current_playlist()
        elif action == 'update':
            self.mpdclient.update_database()
            self.mqtt.publish_msgs(self.mpdclient.get_all_songs_in_db(), topic_name=['music_gateway/pub/database'])

    def select_song_in_playlist(self, desired_song):
        """

        :return:
        """
        for song in self.mpdclient.get_playlist_info():
            if desired_song == song['file']:
                pos = song['pos']
                self.mpdclient.play(songpos=pos)
                break

    def del_song_from_playlist(self, delete_song):
        """

        :return:
        """
        for song in self.mpdclient.get_playlist_info():
            if delete_song == song['file']:
                self.mpdclient.delete_song(songid=song['id'])
                break

    def add_song_from_db(self, add_song):
        """

        :return:
        """
        database = self.mpdclient.get_all_songinfos_from_db()
        for song in database:
            if add_song == song['file']:
                self.mpdclient.add_song_to_playlist(song['file'])
                break






class FindInDatabase:

    def __init__(self, mpdclient, msg):
        """

        :param mpdclient:
        :param msg:
        """
        self.mpdclient = mpdclient
        self.msg = msg

        if isinstance(msg, list):
            for song in msg:
                #self.artist = song.get('artist')
                #self.title = song.get('title')
                self.find_in_database(song.get('title'))

    def find_in_database(self, title):
        """

        :return:
        """
        d = self.mpdclient.advanced_search_in_db(title)
pass
