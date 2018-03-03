try:
    from setuptools import setup
    from setuptools.command.install import install
except ImportError:
    from distutils.core import setup
    from distutils.command.install import install


setup(
    name="music_gateway",
    description="control music over mobile network with the MQTT protocol",
    version="1.0",
    author="Bierschneider Christian",
    author_email="christian.bierschneider@web.de",
    py_modules=["music_gateway"],
    scripts=['scripts/music_gateway.sh'],
    packages=["music", "src", "src.communication", "src.player", "test"],
    package_data={'music': ['mpd.exe', 'songs/*.txt', 'radio_playlists/*.m3u']},
    install_requires=["psutil", "paho-mqtt", "paho-mqtt", "python-mpd2"],
    #cmdclass={
    #    'install': PostInstallCommand
    #}
)

# Dependencies

# pip3 install psutil
# pip3 install python-mpd2
# pip3 install paho-mqtt