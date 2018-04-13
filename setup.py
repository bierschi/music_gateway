try:
    from setuptools import setup
    from setuptools.command.install import install
except ImportError:
    from distutils.core import setup
    from distutils.command.install import install
import platform
from src.settings import Settings
from subprocess import call


class PostInstallCommand(install):

    def run(self):
        system, machine = platform.system(), platform.machine()
        if system == "Windows" and machine in {"i686", "i786", "x86", "x86_64", "AMD64"}:
            Settings()
            install.run(self)
        elif system == "Linux" and machine in {"i686", "i786", "x86", "x86_64", "AMD64"}:
            install.run(self)
            call('pip3 install -r requirements.txt'.split())
            call(['scripts/linux_settings.sh'])



setup(
    name="music_gateway",
    description="control music over mobile network with the MQTT protocol",
    version="1.0",
    author="Bierschneider Christian",
    author_email="christian.bierschneider@web.de",
    py_modules=["music_gateway", "definitions"],
    scripts=['scripts/music_gateway.sh', 'scripts/linux_settings.sh'],
    packages=["music", "src", "src.communication", "src.player", "test"],
    package_data={'music': ['mpd.exe', 'songs/*.txt', 'radio_playlists/*.m3u']},
    install_requires=["psutil", "paho-mqtt", "python-mpd2", "pyserial"],
    cmdclass={
        'install': PostInstallCommand
    },
)



