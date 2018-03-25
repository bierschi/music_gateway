import serial
from time import localtime


class GPS:
    """
    GPS class to parse the NMEA GPS coordinates GPGGA, GPRMC

    Create GPS Instance:
    gps = GPS(port='COM1', baudrate=9600, nmea_type='GPGGA')

    """

    def __init__(self, port, baudrate=None, nmea_type=None):
        """

        constructor to initialize port, baudrate and nmea_type

        :param port: defines the port for the serial connection
        :param baudrate: the baudrate to communicate with the serial interface
        """
        self.port = port

        if baudrate is None:
            self.baudrate = 9600
        else:
            if isinstance(baudrate, int):
                self.baudrate = baudrate
            else:
                raise TypeError("baudrate must be an integer")

        try:
            self.serial_con = serial.Serial(port=self.port, baudrate=self.baudrate, bytesize=serial.EIGHTBITS, parity=serial.PARITY_NONE,
                                            stopbits=serial.STOPBITS_ONE, timeout=None, xonxoff=False, rtscts=False, dsrdtr=False)
        except serial.SerialException as e:
            print(str(e))
            self.serial_con = None

        if nmea_type is not None:
            self.nmea_type = nmea_type
        else:
            self.nmea_type = None

    def __del__(self):
        """
        destructor
        """
        if self.serial_con is not None:
            self.serial_con.close()

    def get_raw_data_list(self):
        """
        get the raw gps data as a list

        :return: a list containing gps raw data
        ['$GPGGA', '131046.00', '4900.12878', 'N', '01205.91768', 'E', '1', '07', '1.44', '437.8', 'M', '46.0', 'M', '', '*5F']
        """
        try:
            if self.serial_con is not None:
                gps_array = str(self.serial_con.readline(), 'utf-8').rstrip().split(',')
            else:
                raise ValueError("Attribute serial_con is None")

            if self.nmea_type is None:
                return gps_array

            elif len(gps_array) == 15 and self.nmea_type == 'GPGGA':
                checksum = ''.join(gps_array[-1:])
                checksum = checksum[-2:]
                assert self.calc_checksum(gps_array) == checksum
                return gps_array

            elif len(gps_array) == 13 and self.nmea_type == 'GPRMC':
                checksum = ''.join(gps_array[-1:])
                checksum = checksum[-2:]
                assert self.calc_checksum(gps_array) == checksum
                return gps_array

            elif len(gps_array) == 18 and self.nmea_type == 'GPGSA':

                return gps_array

        except AssertionError as e:
            print(str(e))
        except UnicodeDecodeError as e:
            print(str(e))

        else:
            return self.get_raw_data_list()

    def get_raw_data_dict(self):
        """
        get the gps raw data as a dictionary

        :return: a dictionary containing gps raw data

        {'longitude': '01205.89493', 'geoidal_seperation': '46.0', 'dilution_of_precision': '1.67',
        'time_utc': '131328.00', 'gps_quality': '1', 'orientation_longitude': 'E', 'checksum': '*53',
        'height_over_msl': '579.4', 'latitude': '4900.14196', 'unit_of_height': 'M', 'number_of_satellites': '07',
        'orientation_latitude': 'N', 'unit_of_geoidal': 'M', 'nmea_type': '$GPGGA'}

        """
        try:

            if self.nmea_type == 'GPGGA':
                return GPGGA(self.get_raw_data_list()).__dict__
            elif self.nmea_type == 'GPRMC':
                return GPRMC(self.get_raw_data_list()).__dict__

        except TypeError as e:
            print(str(e))

    def get_converted_data_dict(self):
        """
        get the converted gps data as a dictionary

        :return: a dictionary containing gps converted data

        {'number_of_satellites': '07', 'time_utc': '123602.00', 'longitude': '12.0993305', 'time_cet': '133602.00',
        'dilution_of_precision': '1.49', 'gps_quality': 'GPS fix', 'geoidal_seperation': '46.0',
        'orientation_latitude': 'North', 'checksum': '*5C', 'latitude': '49.002388833333335', 'orientation_longitude': 'East',
        'unit_of_geoidal': 'M', 'height_over_msl': '412.9', 'unit_of_height': 'M', 'nmea_type': '$GPGGA'}

        """
        try:

            if self.nmea_type == 'GPGGA':
                return GPGGA(self.get_raw_data_list()).__call__()
            elif self.nmea_type == 'GPRMC':
                return GPRMC(self.get_raw_data_list()).__call__()

        except TypeError as e:
            print(str(e))

    def calc_checksum(self, gps_array):
        """
        method to calculated the checksum

        :param gps_array: a List containing the gps data
        :return: the calculated checksum
        """
        s = 0
        line = ','.join(gps_array)
        line.rstrip()
        for c in line[1:-3]:
            s = s ^ ord(c)
        checksum = hex(s)
        checksum = checksum[2:].upper()

        return checksum


class BaseConvert:
    """
    Base class for GPGGA and GPRMC to convert gps data only once
    """

    def __init__(self, time_utc, latitude, orientation_latitude, longitude, orientation_longitude):

        self.time_utc = time_utc
        self.latitude = latitude
        self.orientation_latitude = orientation_latitude
        self.longitude = longitude
        self.orientation_longitude = orientation_longitude

    def get_time(self):
        """
        method to get the time

        :return: time_utc := string '081550.00'
                 time_cet := string '091552.00'
        """
        if self.time_utc is '':
            time_utc = ''
            time_cet = ''
            return time_utc, time_cet
        time_utc = self.time_utc
        time_utc_hours = time_utc[time_utc.find(".") - 6:time_utc.find(".") - 4]

        if localtime().tm_isdst:
            time_cet_hours = int(time_utc_hours)
            time_cet_hours += 2
        else:
            time_cet_hours = int(time_utc_hours)
            time_cet_hours += 1
        time_minutes = time_utc[time_utc.find(".") - 4:time_utc.find(".") - 2]
        time_seconds = time_utc[time_utc.find(".") - 2:time_utc.find(".")]

        time_cet = str(time_cet_hours) + str(time_minutes) + str(time_seconds)
        time_cet = "{:.2f}".format(float(time_cet)).zfill(9)

        return time_utc, time_cet

    def get_latitude(self):
        """
        method to get the latitude coordinates

        :return: latitude := string '23.0024'
        """
        degree_of_latitude = self.latitude

        if degree_of_latitude == '':
            latitude = ''
            return latitude
        else:
            latitude_min = str(float(degree_of_latitude[degree_of_latitude.find(".") - 2:]) / 60)
            latitude_degr = degree_of_latitude[:degree_of_latitude.find(".") - 2]
            latitude = float(latitude_degr) + float(latitude_min)

            return str(latitude)

    def get_orientaton_latitude(self):
        """
        method to get the orientation of latitude coordinates

        :return: orientation latitude := string 'North'
        """
        if self.orientation_latitude == '':
            orientation_latitude = ''
        else:
            if self.orientation_latitude == 'N':
                orientation_latitude = 'North'
            else:
                orientation_latitude = 'South'

        return orientation_latitude

    def get_longitude(self):
        """
        method to get the longitude coordinates

        :return: longitude := string '38.0023'
        """
        degree_of_longitude = self.longitude

        if degree_of_longitude == '':
            longitude = ''
            return longitude
        else:
            longitude_min = str(float(degree_of_longitude[degree_of_longitude.find(".") - 2:]) / 60)
            longitude_degr = degree_of_longitude[:degree_of_longitude.find(".") - 2]
            longitude = float(longitude_degr) + float(longitude_min)

            return str(longitude)

    def get_orientation_longitude(self):
        """
        method to get the orientation of longitude coordinates

        :return: orientation_longitude := string 'East'
        """
        if self.orientation_longitude == '':
            orientation_longitude = ''
        else:
            if self.orientation_longitude == 'E':
                orientation_longitude = 'East'
            else:
                orientation_longitude = 'West'

        return orientation_longitude


class GPGGA(BaseConvert):

    def __init__(self, array):
        """
        fill the gpgga attributes with correct values from given array

        :param array: a List containing the gps raw data

        ['$GPGGA', '131046.00', '4900.12878', 'N', '01205.91768', 'E', '1', '07', '1.44', '437.8', 'M', '46.0', 'M', '', '*5F']

        """

        if len(array) == 15 and isinstance(array, list):
            self.nmea_type = array[0]
            super().__init__(array[1], array[2], array[3], array[4], array[5])
            self.gps_quality = array[6]
            self.number_of_satellites = array[7]
            self.dilution_of_precision = array[8]
            self.height_over_msl = array[9]
            self.unit_of_height = array[10]
            self.geoidal_seperation = array[11]
            self.unit_of_geoidal = array[12]
            self.checksum = array[14]

    def __call__(self):
        """
        callable instance method which returns the converted gps data as dictionary

        :return: gps data as dictionary

        {'time_cet': '091550.00', 'dilution_of_precision': '1.96', 'nmea_type': '$GPGGA', 'time_utc': '081550.00',
        'orientation_latitude': 'North', 'longitude': '12.0997915', 'gps_quality': 'GPS fix',
        'number_of_satellites': '06', 'orientation_longitude': 'East', 'height_over_msl': '377.4', 'checksum': '*50',
         'unit_of_geoidal': 'M', 'geoidal_seperation': '46.0', 'unit_of_height': 'M', 'latitude': '49.0022825'}

        """
        self.gps_dict_converted = {}

        time_utc, time_cet = super().get_time()
        latitude = super().get_latitude()
        orientation_latitude = super().get_orientaton_latitude()
        longitude = super().get_longitude()
        orientation_longitude = super().get_orientation_longitude()

        gps_quality = self.get_gps_quality()
        number_of_satellites = self.get_number_of_satellites()
        dilution_of_precision = self.get_dilution_of_precision()
        height_over_msl = self.get_height_over_msl()
        unit_of_height = self.get_unit_of_height()
        geoidal_seperation = self.get_geoidal_seperation()
        unit_of_geoidal = self.get_unit_of_geoidal()

        self.gps_dict_converted = {
            "nmea_type": self.nmea_type,
            "time_utc": time_utc,
            "time_cet": time_cet,
            "latitude": latitude,
            "orientation_latitude": orientation_latitude,
            "longitude": longitude,
            "orientation_longitude": orientation_longitude,
            "gps_quality": gps_quality,
            "number_of_satellites": number_of_satellites,
            "dilution_of_precision": dilution_of_precision,
            "height_over_msl": height_over_msl,
            "unit_of_height": unit_of_height,
            "geoidal_seperation": geoidal_seperation,
            "unit_of_geoidal": unit_of_geoidal,
            "checksum": self.checksum
        }
        return self.gps_dict_converted

    def get_gps_quality(self):
        """
        method to get the gps quality

        :return: gps_quality := string 'GPS fix'
        """
        if self.gps_quality == "0":
            gps_quality = "GPS invalid"
        elif self.gps_quality == "1":
            gps_quality = "GPS fix"
        elif self.gps_quality == "2":
            gps_quality = "DGPS fix"
        else:
            gps_quality = ""

        return gps_quality

    def get_number_of_satellites(self):
        """
        method to get the number of satellites

        :return: self.number_of_satellites := string '06'
        """
        return self.number_of_satellites

    def get_dilution_of_precision(self):
        """
        method to get the dilution of precision

        :return: self.dilution_of_precision := string '1.96'
        """
        return self.dilution_of_precision

    def get_height_over_msl(self):
        """
        method to get the height over msl

        :return: self.height_over_msl := string '377.7'
        """
        return self.height_over_msl

    def get_unit_of_height(self):
        """
        method to get the unit of height

        :return: self.unit_of_height := string 'M'
        """
        return self.unit_of_height

    def get_geoidal_seperation(self):
        """
        method to get the geoidal seperation

        :return: self.geoidal_seperation := string '46.0'
        """
        return self.geoidal_seperation

    def get_unit_of_geoidal(self):
        """
        method to get the unit fo geoidal seperation

        :return: self.unit_of_geoidal := string 'M'
        """
        return self.unit_of_geoidal


class GPRMC(BaseConvert):

    def __init__(self, array):
        """
        fill the GPRMC attributes with correct values from given array

        :param array: a List containing the gps raw data
        """
        if len(array) == 13 and isinstance(array, list):
            self.nmea_type = array[0]
            super().__init__(array[1], array[3], array[4], array[5], array[6])
            self.state = array[2]
            self.velocity_over_ground = array[7]
            self.course_over_ground = array[8]
            self.date = array[9]
            self.magnetic_deviation = array[10]
            self.sign_of_deviation = array[11]
            self.signal_integrity = array[12]
            self.checksum = self.signal_integrity[1:4]

    def __call__(self):
        """
        callable instance method which returns the converted gps data as dictionary

        :return: gps data as dictionary
        """
        self.gps_dict_converted = {}

        time_utc, time_cet = super().get_time()
        state = self.get_state()
        latitude = super().get_latitude()
        orientation_latitude = super().get_orientaton_latitude()
        longitude = super().get_longitude()
        orientation_longitude = super().get_orientation_longitude()
        velocity_over_ground = self.get_velocity_over_ground()
        course_over_ground = self.get_course_over_ground()
        date = self.get_date()
        magnetic_deviation = self.get_magnetic_deviation()
        sign_of_deviation = self.get_sign_of_deviation()
        signal_integrity = self.get_signal_integrity()

        self.gps_dict_converted = {
            "nmea_type": self.nmea_type,
            "time_utc": time_utc,
            "time_cet": time_cet,
            "state": state,
            "latitude": latitude,
            "orientation_latitude": orientation_latitude,
            "longitude": longitude,
            "orientation_longitude": orientation_longitude,
            "velocity_over_ground": velocity_over_ground,
            "course_over_ground": course_over_ground,
            "date": date,
            "magnetic_deviation": magnetic_deviation,
            "sign_of_deviation": sign_of_deviation,
            "signal_integrity": signal_integrity,
            "checksum": self.checksum
        }
        return self.gps_dict_converted

    def get_state(self):
        """
        method to get the state

        :return: state := string 'OK'
        """
        if self.state == '':
            state = ''
        elif self.state == 'A':
            state = 'OK'
        else:
            state = 'warnings'

        return state

    def get_velocity_over_ground(self):
        """
        method to convert velocity over ground from kn into km/h
        
        :return: velocity_over_ground := string '02.5928' km/h
        """
        if self.velocity_over_ground == '':
            velocity_over_ground = ''
        else:
            velocity_over_ground = float(self.velocity_over_ground) * 1.852

        return str(velocity_over_ground)

    def get_course_over_ground(self):
        """
        method to get course over ground in degree

        :return: self.course_over_ground := string
        """
        return self.course_over_ground

    def get_date(self):
        """
        method to get the current date

        :return: date := string '08.11.17'
        """
        day = self.date[:2]
        month = self.date[2:4]
        year = self.date[4:6]

        return '{}.{}.{}'.format(day, month, year)

    def get_magnetic_deviation(self):
        """
        method to get magnetic deviation

        :return: self.magnetic_deviation := string
        """
        return self.magnetic_deviation

    def get_sign_of_deviation(self):
        """
        method to get the sign of magnetic deviation
        
        :return: self.sign_of_deviation := string
        """
        return self.sign_of_deviation

    def get_signal_integrity(self):
        """
        method to get the signal integrity
        
        :return: signal_integrity := string 'Autonomous mode'
        """
        if self.signal_integrity == '':
            signal_integrity = ''
        else:
            signal_integrity = self.signal_integrity[0:1]

            if signal_integrity == 'A':
                signal_integrity = 'Autonomous mode'
            elif signal_integrity == 'D':
                signal_integrity = 'Differential mode'
            elif signal_integrity == 'E':
                signal_integrity = 'Estimated mode'
            elif signal_integrity == 'M':
                signal_integrity = 'Manual input mode'
            elif signal_integrity == 'S':
                signal_integrity = 'Simulated mode'
            elif signal_integrity == 'N':
                signal_integrity = 'Data not valid'

        return signal_integrity


if __name__ == '__main__':

    gps = GPS(port='COM9', baudrate=9600, nmea_type='GPGGA')

    while True:
        #print(gps.get_raw_data_list())
        #print(gps.get_raw_data_dict())
        gps_dict = gps.get_converted_data_dict()
        time_cet = gps_dict.get('time_cet')
        latitude = gps_dict.get('latitude')
        longitude = gps_dict.get('longitude')
        print("time: {}, longitude: {}, latitude: {}".format(time_cet, longitude, latitude))