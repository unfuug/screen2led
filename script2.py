### Windows compatible script
### Work in progress
### Author: Lutz Warnecke

import time
import serial
from colorthief_modified import ColorThief
from PIL import ImageGrab

DELAY = 0.5

start_marker = 40
end_marker   = 41
separation_marker = 44

def extract_screen_color():
    #start_time = time.time()
    screen = ImageGrab.grab(bbox=(1920, 1080, 2560, 1440))
    palette = ColorThief(screen).get_palette(color_count=5, quality=10)
    # Idea from: https://github.com/fengsp/color-thief-py/issues/17
    color = max(palette, key=lambda i: i[-1])[0:3]
    #print(f"Finish in: {round(1000 * (time.time() - start_time))} ms ") # how much  he takes to finish
    return color

def is_too_samey(rgb, margin):
    r, g, b = rgb

    if ( g - margin <= r <= g + margin and 
         b - margin <= r <= b + margin ):
        return True

    return False

def send_to_arduino(rgb, arduino):
    enc_rgb = encode(rgb)
    arduino.write(enc_rgb)

def encode(rgb):
    r, g, b = rgb
    sep_char = chr(separation_marker)
    enc_rgb = chr(start_marker) + str(r) + sep_char + str(g) + sep_char + str(b) + chr(end_marker)
    return enc_rgb.encode("ascii")

def equal_with_margin(rgb1, rgb2, margin):
    r1, g1, b1 = rgb1
    r2, g2, b2 = rgb2

    if ( r2 - margin <= r1 <= r2 + margin and
         g2 - margin <= g1 <= g2 + margin and 
         b2 - margin <= b1 <= b2 + margin ):
       return True

    return False


def main():
    # Linux:
    # arduino = serial.Serial(port="/dev/ttyACM0", baudrate=9600)
    # Windows:
    arduino = serial.Serial(port="COM3", baudrate=9600)
    time.sleep(3)

    current_color = (0,0,0)

    try: 
        while True:
            color = extract_screen_color()
            print(color)
            if not equal_with_margin(color, current_color, 10):
                print("sending...")
                send_to_arduino(color, arduino)
                current_color = color
            time.sleep(DELAY)
    except KeyboardInterrupt:
        arduino.close()
        print("Successfully exited!")

    

if __name__ == "__main__":
    main()