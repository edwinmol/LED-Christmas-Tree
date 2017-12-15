# this file containes random-point patterns, e.g. voxelRand.

# import fundamental plotting functions, time.sleep, and random.randint
from plot import *

from time import sleep
from random import randint


# fills the tree with random voxels
# because this uses a uniform random distribution, it has to run at a much
# faster speed than other programs to account for the fact that many LEDs are
# being lit multiple times
from patterns.plot import led, fullTree, ledFill, clear


def voxelRand(times, speed):
    speed = speed / 5

    # plot random points to fill the tree
    for t in range(times):
        vX = randint(0, 6)
        vY = randint(0, 7)
        led(vX, vY, randint(0, 15), randint(0, 15), randint(0, 15))
        sleep(speed)
        
    sleep(speed * 2)
    
    # plot random points to empty the cube
    for t in range(times):
        vX = randint(0, 6)
        vY = randint(0, 7)
        led(vX, vY, 0, 0, 0)
        sleep(speed)
        
    # smoothly erase any remaining points
    for l in range(8):
        ledFill(0, l, 6, l, 0, 0, 0)
        sleep(speed * 2)
    clear()
    
    sleep(speed)


# makes a simple firework-like effect
def firework(times, speed):
    for t in range(times):
        stars = []
        r = randint(0, 15)
        g = randint(0, 15)
        b = randint(0, 15)

        # draw the firework spiraling up into the 'sky'
        for n in range(8):
            clear()
            led(0, n, r, g, b)
            sleep(speed)

        for n in range(8):
            lay = 7 - n
            clear()
            ledFill(1, lay, 6, lay, r, g, b)
            sleep(speed)

        # create random firework star 'twinkles'
        clear()
        for n in range(randint(6, 9)):
            stars.append([randint(0, 6), randint(5, 7), randint(0, 15), randint(0, 15), randint(0, 15)])

        # move stars down to the ground
        while stars != []:
            for s in stars:
                led(s[0], s[1], s[2], s[3], s[4])
                if s[1] < 7:
                    led(s[0], s[1]+1, 0, 0, 0)
                
                if s[1] > 0:
                    s[1] -= 1
                else:
                    stars.remove(s)
                sleep(speed / 4)
