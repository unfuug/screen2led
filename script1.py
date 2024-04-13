import time
import sched
import serial
import colorsys
from colorthief_modified import ColorThief
#import pyscreenshot as ImageGrab
#from PIL import ImageGrab
#from mss.linux import MSS as mss
from pylette_modified.color_extraction import extract_colors
from pylette_modified.color import Color

DELAY = 0.5

start_marker = 40
end_marker   = 41
separation_marker = 44

def extract_screen_color():

    #start_time = time.time()
    bbox = (1920, 1080, 2560, 1440)
    screen = ImageGrab.grab(bbox, backend="freedesktop_dbus")
    color_thief: ColorThief = ColorThief(screen)
    palette: list = color_thief.get_palette(color_count=5, quality=20)
    #palette = extract_colors(screen, palette_size=10, resize=True, mode='MC', sort_mode='luminance')
    # Idea from: https://github.com/fengsp/color-thief-py/issues/17
    color = max(palette, key=lambda i: i[-1])[0:3]
    #palette.sort(key=lambda i: i[-1])
    # Maybe it is a good idea to select a highlight color when
    # the base color is too dark or grayish/white.
    # for color in palette:
    #     if not is_too_samey(color.rgb, 40):
    #         return boost_saturation(color.rgb)

    #return boost_saturation(palette[0].rgb)
    return color
    #print(f"Finish in: {round(1000 * (time.time() - start_time))} ms ") # how much  he takes to finish

# takes an RGB color, boosts saturation in HSV and returns the color in RGB
def boost_saturation(rgb):
    r, g, b = rgb
    h, s, v = colorsys.rgb_to_hsv(r/255, g/255, b/255)

    print((h,s,v))
    print(colorsys.hsv_to_rgb(h, 1, v))

    r, g, b = colorsys.hsv_to_rgb(h, 1, v)

    return (r*255,g*255,b*255)



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
    arduino = serial.Serial(port="/dev/ttyACM0", baudrate=9600)
    time.sleep(3)

    # my_scheduler = sched.scheduler(time.time, time.sleep)
    # my_scheduler.enter(DELAY, 1, loop, (my_scheduler,))
    # my_scheduler.run()

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

    

if __name__ == "__main__":
    main()