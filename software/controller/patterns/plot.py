# this file contains the fundamental plotting functions; all other patterns
# should use these to write to the 'points' list

# import points list
from core import points
from core import Bam_filler


bam = Bam_filler


# fills a specific LED with rgb
def led(x, y, r, g, b):
    points[y][x][0] = r
    points[y][x][1] = g
    points[y][x][2] = b
    bam.fill()


# fills from (x1,y1,z1) to (x2,y2,z2) with rgb
def ledFill(x1, y1, x2, y2, r, g, b):
    # if point1 > point2, swap them
    if x1 > x2:
        x2Old = x2
        x2 = x1
        x1 = x2Old
        
    if y1 > y2:
        y2Old = y2
        y2 = y1
        y1 = y2Old
        
    # fill in points
    for y in range(y1, y2+1):
        for x in range(x1, x2+1):
            led(x, y, r, g, b)


# a quick and easy way to use ledFill to light the whole tree in a specific rgb color
def fullTree(r=0, g=0, b=0):
    ledFill(0, 0, 6, 7, r, g, b)


# a quick and easy way to use ledFill to light the whole tree in red
def fullRedTree():
    fullTree(15, 0, 0)


# a quick and easy way to use ledFill to light the whole tree in green
def fullGreenTree():
    fullTree(0, 15, 0)


# a quick and easy way to use ledFill to light the whole tree in blue
def fullBlueTree():
    fullTree(0, 0, 15)


# and a quick way to clear the whole tree
def clear():
    ledFill(0, 0, 6, 7, 0, 0, 0)
