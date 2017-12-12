"""--------------IMPORT MODULES--------------"""
import RPi.GPIO as GPIO
import threading
from time import sleep

"""-------------CLASS DEFINITIONS----------------"""
#sequence class, used to run through patterns defined in LEDcube.py
class Sequence():

    #inputs a list of sublists, where each sublist contains three pattern
    #   elements: the functions, its name parameter, and the number of repetitions
    def __init__(self, patterns):
        self.patterns = []

        for p in range(len(patterns)):
            self.patterns.append(patterns[p])

    #adds a single pattern sublist
    def add(self, pattern):
        self.patterns.append(pattern)

    #run the sequence for times iterations
    def run(self, times, speed):
        t = times
        while t > 0:

            #for every sublist
            for p in range(len(self.patterns)):
                #if the sublist contains real parameters, apply them
                if not self.patterns[p][1] == "N":
                    self.patterns[p][0](self.patterns[p][1],
                                        self.patterns[p][2],
                                        speed)

                #otherwise run without a parameter
                else:
                    self.patterns[p][0](self.patterns[p][2], speed)

            #if t > 9999 then run the sequence forever
            if not t > 9999:
                t -= 1
