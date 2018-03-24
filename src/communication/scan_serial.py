import sys
import glob
import serial
import errno


class ScanSerial:

    def __init__(self):
        """

        """
        self.available = []
        self.possible_ports = []
        self.serial_port = None
        self.gps_dataformats = [b'$GPRMC', b'$GPGGA', b'$GPGSA']

        if sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
            self.possible_ports += glob.glob("/dev/rfcomm[0-9]*")
            self.possible_ports += glob.glob("/dev/ttyUSB[0-9]*")

        elif sys.platform.startswith('win'):
            self.possible_ports += ["\\.\COM%d" % i for i in range(256)]

        elif sys.platform.startswith('darwin'):
            exclude = [
                '/dev/tty.Bluetooth-Incoming-Port',
                '/dev/tty.Bluetooth-Modem'
            ]
            self.possible_ports += [port for port in glob.glob('/dev/tty.*') if port not in exclude]

    def get_gps_port(self):
        """
        returns the port where the gps is connected

        :return: gps port as string
        """
        for port in self.available_ports():
            self.serial_port = serial.Serial(port=port)
            self.serial_port.timeout = 1
            line = self.serial_port.readline()
            for dataformat in self.gps_dataformats:
                if dataformat in line:
                    self.serial_port.close()
                    return port

    def try_port(self, port_str):
        """
        returns boolean for port availability
        """
        try:
            s = serial.Serial(port_str)
            s.close()
            return True

        except serial.SerialException:
            pass
        except OSError as e:
            if e.errno != errno.ENOENT:
                raise e

        return False

    def available_ports(self):
        """
        creates a list with available ports

        :return: list with available ports
        """
        for port in self.possible_ports:
            if self.try_port(port):
                self.available.append(port)

        return self.available

