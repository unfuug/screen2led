from connections.connection import ConnectionInterface
from serial import Serial, SerialException 
from connections.lib import is_valid_color

class ArduinoConnection(ConnectionInterface):
    """A class implementing a connection to an Arduino.
    
    Attributes
    ----------
    port : string
        The Port on which to connect to the Arduino.
    baudrate : int
        Baudrate the Arduino is set to.
    Verbosity : Boolean, optional
        Print information to stdout for debuging (default: False)
    """

    def __init__(self, port, baudrate, verbosity = False):
        self.port              = port
        self.baudrate          = baudrate
        self.verbosity         = verbosity

        self.__arduino = None

        self.__device_name       = "Arduino Uno"
        self.__start_marker      = chr(40)
        self.__end_marker        = chr(41)
        self.__separation_marker = chr(44)

    def __str__(self):
        return f"{self.__device_name} (Port: {self.port}, Baudrate: {self.baudrate})"
    
    def open(self):
        if self.__arduino is not None:
            print(f"Already connected to {self}.")
            return
        try:
            self.__arduino = Serial(port=self.port, baudrate=self.baudrate)
        except SerialException:
            print(f"Cannot connect to {self}. Are you sure the Arduino is connected?")


    def send(self, color):
        if self.__arduino == None:
            print(f"Not connected to {self}. Use open() method to establish connection.")
            return

        if not is_valid_color(color):
            print("Invalid color. Color is expected to be a tuple (r,g,b) with rgb ∈ {0,..,255}")
            return
        
        enc_rgb = self.__encode(color)
        self.__arduino.write(enc_rgb)
        if self.verbosity:
            print(f"Send color: {color}")

    def close(self):
        if self.__arduino == None:
            print(f"Cannot close connection. Not connected to {self}. Use open() method first.")
            return
        self.__arduino.close()
        self.__arduino = None
        if self.verbosity:
            print(f"Connection to {self} succesfully closed!")

    def __encode(self, color):
        r, g, b = color
        enc_rgb = self.__start_marker + str(r) \
                + self.__separation_marker + str(g) \
                + self.__separation_marker + str(b) \
                + self.__end_marker
        return enc_rgb.encode("ascii")
    