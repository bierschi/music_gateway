import sys
import glob
import serial
import errno


class ScanSerial:

    _TRY_BAUDS = [4800, 7200, 9600, 14400, 19200, 38400, 57600, 115200]

    def __init__(self, baudrate=None):
        """

        """
        self.available = []
        self.possible_ports = []
        self.gps_nmea = [b'$GPRMC', b'$GPGGA', b'$GPGSA']

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

        """   
        try:
            self.set_baudrate(baudrate)
        except:
            raise ValueError
        """

    def get_gps_port(self):
        """

        :return:
        """
        for port in self.available_ports():
            self.port = serial.Serial(port=port)
            line = self.port.readline()
            for gps in self.gps_nmea:
                if gps in line:
                    self.port.close()
                    return port

    def try_port(self, port_str):
        """
        returns boolean for port availability
        """
        try:
            s = serial.Serial(port_str)
            s.close()  # explicit close 'cause of delayed GC in java
            return True

        except serial.SerialException:
            pass
        except OSError as e:
            if e.errno != errno.ENOENT: # permit "no such file or directory" errors
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

    def set_baudrate(self, baudrate):
        """

        :param baudrate:
        :return:
        """
        if baudrate is None:
            self.baudrate = self.auto_baudrate()
        else:
            self.baudrate = baudrate

    def auto_baudrate(self):
        """

        :return:
        """
        gps_nmea = {b'$GPRMC', b'$GPGGA'}
        self.port.timeout = 1
        for baud in self._TRY_BAUDS:
            self.port.baudrate = baud


if __name__ == '__main__':
    ports = ScanSerial()
    #ports = ports.available_ports()
    #print(ports)
    #ser = serial.Serial(ports[0], baudrate=9600)
    #while True:
    #    print(ser.readline())