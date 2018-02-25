

class ControlMPD:

    def __init__(self, mpdclient, msg):
        """

        :param mpdclient:
        :param msg:
        """
        self.mpdclient = mpdclient
        self.msg = msg
        if self.msg in {'play', 'stop', 'previous', 'pause', 'next', 'shuffle'}:
            self.handle_playback(self.msg)
        elif self.msg in {'random', 'repeat'}:
            self.handle_playback_option(self.msg)

    def handle_playback(self, msg):
        """

        :param msg:
        :return:
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

        :param msg:
        :return:
        """
        if msg == 'random':
            self.mpdclient.set_random()
        elif msg == 'repeat':
            self.mpdclient.set_repeat()
