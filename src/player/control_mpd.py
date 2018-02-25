

class ControlMPD:

    def __init__(self, mpdclient, msg):
        """
        constructor to handle the mpd playback
        :param mpdclient: instance for the mpd
        :param msg: msg string like 'play', 'stop' ...
        """
        self.mpdclient = mpdclient
        self.msg = msg
        if self.msg in {'play', 'stop', 'previous', 'pause', 'next', 'shuffle'}:
            self.handle_playback(self.msg)
        elif self.msg in {'random', 'repeat', 'clear', 'update'}:
            self.handle_playback_option(self.msg)

    def handle_playback(self, msg):
        """
        method to handle simple playback option

        :param msg: msg string like 'play', 'stop' ...
        """

        if msg == 'play':
            self.mpdclient.play()
        elif msg == 'stop':
            self.mpdclient.stop()
        elif msg == 'next':
            self.mpdclient.next()
        elif msg == 'pause':
            self.mpdclient.pause()
        elif msg == 'previous':
            self.mpdclient.previous()
        elif msg == 'shuffle':
            self.mpdclient.shuffle()

    def handle_playback_option(self, msg):
        """
        method to handle advanced playback option

        :param msg: msg string like 'random', 'repeat' ...
        """
        if msg == 'random':
            self.mpdclient.set_random()
        elif msg == 'repeat':
            self.mpdclient.set_repeat()
        elif msg == 'clear':
            self.mpdclient.clear_current_playlist()
        elif msg == 'update':
            self.mpdclient.update_database()


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
