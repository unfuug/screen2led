import serial

class Connection:
    """
    TODO
    """

    start_marker      = chr(40)
    end_marker        = chr(41)
    separation_marker = chr(44)

    device = "Arduino Uno"

    def __init__(self, port, baudrate, verbosity = False):
        self.port = port
        self.baudrate = baudrate
        self.verbosity = verbosity

        # Connect to Arduino
        self.__arduino = serial.Serial(port=self.port, baudrate=self.baudrate)

    def __str__(self):
        return f"Connection to {self.device} (Port: {self.port}, Baudrate: {self.baudrate})"

    def send(self, color):
        if not self.__is_valid_color(color):
            if self.verbosity: 
                print(f"{color} is not a valid color and can't be send!")
            return
        
        enc_rgb = self.__encode(color)
        self.__arduino.write(enc_rgb)
        if self.verbosity:
            print(f"Send color: {color}")

    def close(self):
        self.__arduino.close()
        if self.verbosity:
            print(f"{self} succesfully closed!")

    def __encode(self, color):
        r, g, b = color
        enc_rgb = self.start_marker + str(r) \
                + self.separation_marker + str(g) \
                + self.separation_marker + str(b) \
                + self.end_marker
        return enc_rgb.encode("ascii")
    
    def __is_valid_color(self, color):
        if type(color) is not tuple:
            return False
        if not len(color) == 3:
            return False
        
        for c in color:
            if type(c) is not int or (0 > c) or (c > 255):
                return False
        
        return True
    