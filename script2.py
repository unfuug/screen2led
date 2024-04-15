### Windows compatible script
### Work in progress
### Author: Lutz Warnecke

import time
import math
import serial
from colorthief_modified import ColorThief
from connections.arduino import ArduinoConnection
from PIL import ImageGrab

def extract_screen_color():

    # TODO/ IDEA: Use Pylette (https://github.com/qTipTip/Pylette) and filter
    # output palette for a good highlight color, thats not too grayish.

    #start_time = time.time()
    screen = ImageGrab.grab(bbox=(1920, 1080, 2560, 1440))
    palette = ColorThief(screen).get_palette(color_count=5, quality=10)
    # Idea from: https://github.com/fengsp/color-thief-py/issues/17
    color = max(palette, key=lambda i: i[-1])[0:3]
    #print(f"Finish in: {round(1000 * (time.time() - start_time))} ms ") # how much  he takes to finish
    return color

def equal_with_margin(rgb1, rgb2, margin):
    r1, g1, b1 = rgb1
    r2, g2, b2 = rgb2
    rd = r1 - r2
    gd = g1 - g2
    bd = b1 - b2

    l2_distance = math.sqrt(rd * rd + gd * gd + bd * bd)
    if ( l2_distance <= margin ):
       return True

    return False


def main():

    DELAY = 0.5
    DEBUG = True
    CONN  = ArduinoConnection(port="COM3", baudrate=9600, verbosity=DEBUG)

    current_color = (0,0,0)

    try: 
        CONN.open()
        while True:
            color = extract_screen_color()
            #if DEBUG: print(color)
            if not equal_with_margin(color, current_color, 10):
                CONN.send(color)
                current_color = color
            time.sleep(DELAY)
    except KeyboardInterrupt:
        pass
    finally:
        print("Exiting...")
        CONN.close()

    

if __name__ == "__main__":
    main()