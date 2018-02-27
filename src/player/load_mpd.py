import platform
import os
import subprocess
import signal
import psutil


class LoadMPD:

    def __init__(self):
        """
        constructor to init variables and call the self.get_os() method
        """
        self.mpd_pid = None
        self.system = platform.system()
        self.machine = platform.machine()

        self.find_os()

    def __del__(self):
        """
        destructor
        """

    def find_os(self):
        """
        depending on the system and machine load the correct mpd server
        """
        base_path = os.path.abspath(os.path.dirname(""))

        if self.system == "Windows" and self.machine in {"i686", "i786", "x86", "x86_64", "AMD64"}:
            self.create_files(base_path)
            mpd_exe_path = os.path.join(base_path, "music\mpd.exe")
            mpd_conf_path = os.path.join(base_path, "music\mpd.conf")
            # bsp = os.path.join(os.getcwd(), "music\mpd.exe")

            if not self.is_mpd_running():
                print("start mpd.exe")
                self.start_mpd_windows(mpd_exe_path, mpd_conf_path)
            else:
                print("mpd.exe is running")

        elif self.system == "Linux" and self.machine in {"i686", "i786", "x86", "x86_64", "AMD64"}:
            if not self.is_mpd_running_linux():
                self.start_mpd_linux()
            else:
                print("mpd already running")

        """
        elif system == "Darwin" and machine in {"i686", "i786", "x86", "x86_64", "AMD64"}:
            flac_converter = os.path.join(base_path, "flac-mac")

        """
    # Windows machines

    def create_files(self, base_path):
        """
        method to check if mpd.conf, mpd.log, mpd.db are exists. If not, then create these files

        :param base_path, path for creating these files
        """
        music_directory = os.path.join(base_path, 'music\songs')
        playlist_directory = os.path.join(base_path, 'music\\radio_playlists')
        mpd_conf_path = os.path.join(base_path, 'music\mpd.conf')

        mpd_log_path = os.path.join(base_path, 'music\mpd.log')
        mpd_log_path = '/'.join(mpd_log_path.split('\\'))
        mpd_db_path = os.path.join(base_path, 'music\mpd.db')
        mpd_db_path = '/'.join(mpd_db_path.split('\\'))

        if not os.path.exists(mpd_log_path):
            open(mpd_log_path, 'w')
        if not os.path.exists(mpd_db_path):
            open(mpd_db_path, 'w')
        if not os.path.exists(mpd_conf_path):
            with open(mpd_conf_path, 'w') as mpd_conf:
                mpd_conf.writelines("music_directory " + "\"" + music_directory + "\"" + "\n" +
                                    "playlist_directory " + "\"" + playlist_directory + "\"" + "\n" +
                                    "log_file " + "\"" + mpd_log_path + "\"" + "\n" +
                                    "db_file " + "\"" + mpd_db_path + "\"" + "\n" + "\n")

                mpd_conf.writelines("audio_output {" + "\n" + "    type \"winmm\"" + "\n" + "    name \"Speakers\"" + "\n" +
                                    "    device \"Lautsprecher (High Definition Audio-Gerät)\"" + "\n" + "}" + "\n")

                mpd_conf.writelines("audio_output {" + "\n" + "    type \"httpd\"" + "\n" + "    name \"My HTTP Stream\"" + "\n"
                                      "    encoder \"vorbis\" # optional, vorbis or lame" + "\n" + "    port \"8000\"" + "\n"
                                    + "    # quality \"5.0\" # do not define if bitrate is defined" + "\n"
                                    + "    bitrate \"128\" # do not define if quality is defined" + "\n"
                                    + "    format \"44100:16:1\"" + "\n" + "}")

    @staticmethod
    def is_mpd_running():
        """
        checks if the mpd server is already running

        :return: "False" if no mpd.exe is running
        """
        return "mpd.exe" in (p.name() for p in psutil.process_iter())

    def start_mpd_windows(self, mpd_exe_path, mpd_conf_path):
        """
        starts the mpd.exe as a background process on windows machines

        :param mpd_exe_path: path to the ./mpd.exe file
        :param mpd_conf_path: path to the ./mpd.conf configuration file
        """
        DETACHED_PROCESS = 0x00000008
        self.mpd_pid = subprocess.Popen([mpd_exe_path, mpd_conf_path], creationflags=DETACHED_PROCESS).pid

    def kill_mpd_process(self):
        """
        method to kill the mpd process with the pid
        :return:
        """
        if self.mpd_pid is not None:
            os.kill(self.mpd_pid, signal.SIGTERM)

    # linux machines

    @staticmethod
    def is_mpd_running_linux():
        """
        checks if the mpd server is already running
        :return:
        """
        return "mpd" in (p.name() for p in psutil.process_iter())

    def start_mpd_linux(self):
        """

        :return:
        """
        p = subprocess.Popen(["apt", "list", "mpd"], stdout=subprocess.PIPE)
        outs, errs = p.communicate()
        if errs is None:
            if b"installed" in outs:
                print("mpd package is installed")
                if not self.is_mpd_running_linux():
                    print("start mpd service")
                    subprocess.call(["sudo", "service", "mpd", "start"])
            else:
                print("install package mpd")
                subprocess.call(["sudo", "apt-get", "install", "mpd"])
        else:
            print("errs")

        #self.mpd_pid = subprocess.Popen([mpd_exe_path, mpd_conf_path], creationflags=DETACHED_PROCESS).pid

