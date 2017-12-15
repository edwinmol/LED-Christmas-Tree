# this file contains geometric shape-related patterns, i.e. patterns that draw
# or manipulate geometric shapes more complicated than lines and planes

# import fundamental plotting functions, time.sleep, and random.randint
from patterns.plot import *

from time import sleep
from random import randint

# lights a wireframe cube at the specified point of the specified size


# entire tree lights up
def tree(time):
    for r in range(16):
        for g in range(16):
            for b in range(16):
                clear()
                ledFill(0, 0, 6, 7, r, g, b)
                sleep(time)


# spins a point in circles to create a cylinder, then repeats to erase itself
def spiral(times, speed):
    # this function naturally runs slower than most, so speed is divided by 2
    # to normalize speed
    speed = speed/2
    
    clear()
    for t in range(times):
        # alternate between RGB colors
        for v in range(3):

            # draw the spiraling point, then move up a layer
            for l in range(8):
                for c in range(7):
                    led(c, l, 15 if v == 0 else 0, 15 if v == 1 else 0, 15 if v == 2 else 0)
                    sleep(speed)


def snake(times, speed):
    # this function naturally runs slower than most, so speed is divided by 2
    # to normalize speed
    speed = speed/2

    clear()
    for t in range(times):
        # alternate between RGB colors
        for v in range(3):

            # draw the circle point, then move up a layer
            for l in range(8):
                for c in range(6):
                    led(c+1, l, 15 if v == 0 else 0, 15 if v == 1 else 0, 15 if v == 2 else 0)
                    sleep(speed)

            for layer in range(8):
                lay = 7 - layer
                led(0, lay, 15 if v == 0 else 0, 15 if v == 1 else 0, 15 if v == 2 else 0)
                sleep(speed)
