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
        self.get_os()

    def __del__(self):
        """
        destructor
        """

    def get_os(self):
        """
        depending on the machine load the correct mpd server
        """
        base_path = os.path.abspath(os.path.dirname(""))
        system, machine = platform.system(), platform.machine()

        if system == "Windows" and machine in {"i686", "i786", "x86", "x86_64", "AMD64"}:
            mpd_exe_path = os.path.join(base_path, "music\mpd.exe")
            mpd_conf_path = os.path.join(base_path, "music\mpd.conf")
            # bsp = os.path.join(os.getcwd(), "music\mpd.exe")

            if not self.is_mpd_running():
                print("start mpd.exe")
                self.start_mpd_windows(mpd_exe_path, mpd_conf_path)
            else:
                print("mpd.exe is running")

        """  
        elif system == "Linux" and machine in {"i686", "i786", "x86", "x86_64", "AMD64"}:
            flac_converter = os.path.join(base_path, "flac-linux-x86")
         
        elif system == "Darwin" and machine in {"i686", "i786", "x86", "x86_64", "AMD64"}:
            flac_converter = os.path.join(base_path, "flac-mac")

        """

    @staticmethod
    def is_mpd_running():
        """
        checks if a mpd.exe is already running

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

    def start_mpd_linux(self):
        """

        :return:
        """

