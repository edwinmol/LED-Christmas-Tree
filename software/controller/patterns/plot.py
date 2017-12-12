#this file contains the fundamental plotting functions; all other patterns
#   should use these to write to the 'points' list

#import points list
from core import points

#sets a specific LED high or low
# def plot(x, y, z, n=1):
def led(x, y, r, g, b):
    points[y][x][0] = r
    points[y][x][1] = g
    points[y][x][2] = b

#fills from (x1,y1,z1) to (x2,y2,z2) with n
# def plotFill(x1, y1, z1, x2, y2, z2, n=1):
def ledFill(x1, y1, x2, y2, r, g, b):
    #if point1 > point2, swap them
    if x1 > x2:
        x2Old = x2
        x2 = x1
        x1 = x2Old
        
    if y1 > y2:
        y2Old = y2
        y2 = y1
        y1 = y2Old
        
    #fill in points
    for y in range(y1, y2+1):
        for x in range(x1, x2+1):
            led(x, y, r, g, b)

#a quick and easy way to use ledFill to light the whole cube in red
def fullCube(r=0, g=0, b=0):
    ledFill(0, 0, 6, 7, r, g, b)

#a quick and easy way to use ledFill to light the whole cube in red
def fullRedCube():
    fullCube(1, 0, 0)

#a quick and easy way to use ledFill to light the whole cube in green
def fullGreenCube():
    fullCube(0, 1, 0)

#a quick and easy way to use ledFill to light the whole cube in blue
def fullBlueCube():
    fullCube(0, 0, 1)

#and a quick way to clear the whole cube
def clear(r=0, g=0, b=0):
    ledFill(0, 0, 6, 7, r, g, b)
    
