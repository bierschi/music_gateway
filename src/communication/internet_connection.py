from http import client
from platform import system
from time import sleep
import socket
import threading


class InternetConnection:

    def __init__(self):
        """

        """
        self.__thread = None
        self.__running = False
        self.platform = system()

    def __del__(self):
        """
        destructor
        """
        self.stop()

    @staticmethod
    def have_internet():
        """
        static method to check if internet connection is available
        it will be faster to just make a HEAD request

        :return: boolean True, if internet available
                 boolean False, if no internet available
        """

        conn = client.HTTPConnection("www.google.com")
        try:
            conn.request("HEAD", "/")
            return True
        except socket.gaierror as e:
            print(str(e) + ": no internet connection available")
            return False

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

    def stop(self):
        """
        method to stop the thread
        """
        if self.__thread is not None:
            self.__running = False
            self.__thread.join()
            self.__thread = None

    def __run(self):
        """


        """
        while self.__running:
            print("run")
            sleep(1)

if __name__ == '__main__':
    ic = InternetConnection()
    print(ic.have_internet())
    ic.start()
    while True:
        pass
