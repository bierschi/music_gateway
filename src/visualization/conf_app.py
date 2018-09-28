import sys
import os
import json
import errno
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow

from definitions import ROOT_DIR
from src.visualization.broker_settings import Ui_MainWindow


class ConfApp(Ui_MainWindow):

    def __init__(self):
        Ui_MainWindow.__init__(self)

        app = QApplication(sys.argv)
        window = QMainWindow()
        self.setupUi(window)
        window.show()

        self.create_conf_file_pb.clicked.connect(self.create_conf_file)
        self.quit_pb.clicked.connect(self.quit)

        app.exec_()

    def create_conf_file(self):
        host = self.host_le.text()
        port = self.port_le.text()
        username = self.username_le.text()
        password = self.password_le.text()
        topic = self.topic_name_le.text()

        self.create_json(host, port, username, password, topic)

        msgBox = QtWidgets.QMessageBox()
        msgBox.setWindowTitle('INFO')
        msgBox.setIcon(QtWidgets.QMessageBox.Information)
        msgBox.setText("Successfully created the configuration file. \n\n (changes can be made in music_gateway-1.0/configs/configuration.json)")
        msgBox.exec_()

    def create_json(self, host, port, username, password, topic):
        conf_file = json.dumps({
            "MQTT": {
                "host": host,
                "port": port,
                "username": username,
                "password": password
            },
            "TOPIC_NAME": {
                "topic": topic
            }
        }, indent=4)
        try:
            os.chdir(ROOT_DIR)
            if not os.path.exists('configs'):
                os.makedirs('configs')
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise

        with open('configs/configuration.json', 'w') as json_file:
            json_file.write(conf_file)

    def quit(self):
        sys.exit(0)


if __name__ == '__main__':
    confApp = ConfApp()
