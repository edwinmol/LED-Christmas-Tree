# this file contains plane-related patterns, e.g. patterns that bounce planes
# across the cube or spin them around the cube

# import fundamental plotting functions and time.sleep
from patterns.plot import fullTree, ledFill

from time import sleep


# bounces a plane along the specified axis
def bounce(axis, times, speed):
    for t in range(times):
        for v in range(3):
            # move the plane along in one direction
            if axis == "x":
                for n in range(7):
                    fullTree(0, 0, 0)
                    ledFill(n, 0, n, 7, 15 if v == 0 else 0, 15 if v == 1 else 0, 15 if v == 2 else 0)
            elif axis == "y":
                for n in range(8):
                    fullTree(0, 0, 0)
                    ledFill(0, n, 6, n, 15 if v == 0 else 0, 15 if v == 1 else 0, 15 if v == 2 else 0)
                sleep(speed)

            # send the plane back
            if axis == "x":
                for n in range(7):
                    fullTree(0, 0, 0)
                    ledFill(6-n, 0, 6-n, 7, 15 if v == 0 else 0, 15 if v == 1 else 0, 15 if v == 2 else 0)
            elif axis == "y":
                for n in range(8):
                    fullTree(0, 0, 0)
                    ledFill(0, 7-n, 6, 7-n, 15 if v == 0 else 0, 15 if v == 1 else 0, 15 if v == 2 else 0)
                sleep(speed)
