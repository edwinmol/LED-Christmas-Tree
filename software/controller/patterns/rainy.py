# this file contains "rainy" patterns, e.g. rain and voxelSend

# import fundamental plotting functions, time.sleep, and random.randint
from plot import *

from time import sleep
from random import randint


# sends random voxels down the y axis, like a rain shower
# this is a slightly resource-demanding program, so it runs at double speed
# has variants 'rain' and 'snow'
from patterns.plot import ledFill, led


def rain(snow=False, times=1, speed=0.075):
    speed = speed / 2
    drops = []
    
    for t in range(times):
        #create a new drop
        rX = randint(0, 3)
        rZ = randint(0, 3)
        drops.append([rX, 3, rZ])
        
        #for each raindrop
        for d in drops:
            #move the drop down one voxel, and erase its old position
            if d[1] < 3:
                plot(d[0], d[1]+1, d[2], 0)
            plot(d[0], d[1], d[2])
            sleep(speed)
            
            #if it hits the ground, stop updating it
            if d[1] == 0:
                if not snow == True and not snow == "snow":
                    plot(d[0], d[1], d[2], 0)
                drops.remove(d)
            d[1] -= 1
            
        sleep(speed)


# sends random voxels up and down the cube
def voxelSend(times, speed):
    r = randint(0, 15)
    g = randint(0, 15)
    b = randint(0, 15)

# fill the top and bottom layers
    ledFill(0, 0, 6, 0, r, g, b)
    ledFill(0, 7, 6, 7, r, g, b)
    sleep(speed)
    
    for t in range(times):
        # select a new point
        vX = randint(0, 6)
        vY = randint(0, 1) * 7

        # send it up or down the cube, depending on its starting y-position
        for n in range(8):
            if vY == 0:
                if n > 0:
                    led(vX, n-1, 0, 0, 0)
                led(vX, n, r, g, b)
                
            elif vY == 7:
                if n > 0:
                    led(vX, (7-n)+1, 0, 0, 0)
                led(vX, (7-n), r, g, b)
            
            sleep(speed)
