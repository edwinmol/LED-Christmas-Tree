"""--------------IMPORT MODULES--------------"""
import RPi.GPIO as GPIO
import threading
from time import sleep

#code designed for a 5 * 8 christmas tree

#these are the core functions, imported to LEDcube.py, which contains the
#   main program operations

"""--------------SETUP VARIABLES AND GPIOS---------------"""
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)

#setup GPIO outputs
pins = [
    # layers (works with multiplexer on controller)
    11, #pin 17, transistor 1 multiplexer (first bit)
    13, #pin 27, transistor 2 multiplexer (second bit)
    15, #pin 22, transistor 3 multiplexer (third bit)

    # columns (uses SPI)
    23, #pin 11, shift register SPI CLOCK
    24, #pin 8, shift register SPI LATCH
    19, #pin 10, shift register SPI SERIAL DATA
]

transistors = [11, 13, 15]

for pin in pins:
    GPIO.setup(pin, GPIO.OUT)

#three-dimensional list containing LED point values
points = [[[0x0, 0x0, 0x0], [0x0, 0x0, 0x0], [0x0, 0x0, 0x0], [0x0, 0x0, 0x0], [0x0, 0x0, 0x0], [0x0, 0x0, 0x0], [0x0, 0x0, 0x0]],
          [[0x0, 0x0, 0x0], [0x0, 0x0, 0x0], [0x0, 0x0, 0x0], [0x0, 0x0, 0x0], [0x0, 0x0, 0x0], [0x0, 0x0, 0x0], [0x0, 0x0, 0x0]],
          [[0x0, 0x0, 0x0], [0x0, 0x0, 0x0], [0x0, 0x0, 0x0], [0x0, 0x0, 0x0], [0x0, 0x0, 0x0], [0x0, 0x0, 0x0], [0x0, 0x0, 0x0]],
          [[0x0, 0x0, 0x0], [0x0, 0x0, 0x0], [0x0, 0x0, 0x0], [0x0, 0x0, 0x0], [0x0, 0x0, 0x0], [0x0, 0x0, 0x0], [0x0, 0x0, 0x0]],
          [[0x0, 0x0, 0x0], [0x0, 0x0, 0x0], [0x0, 0x0, 0x0], [0x0, 0x0, 0x0], [0x0, 0x0, 0x0], [0x0, 0x0, 0x0], [0x0, 0x0, 0x0]],
          [[0x0, 0x0, 0x0], [0x0, 0x0, 0x0], [0x0, 0x0, 0x0], [0x0, 0x0, 0x0], [0x0, 0x0, 0x0], [0x0, 0x0, 0x0], [0x0, 0x0, 0x0]],
          [[0x0, 0x0, 0x0], [0x0, 0x0, 0x0], [0x0, 0x0, 0x0], [0x0, 0x0, 0x0], [0x0, 0x0, 0x0], [0x0, 0x0, 0x0], [0x0, 0x0, 0x0]],
          [[0x0, 0x0, 0x0], [0x0, 0x0, 0x0], [0x0, 0x0, 0x0], [0x0, 0x0, 0x0], [0x0, 0x0, 0x0], [0x0, 0x0, 0x0], [0x0, 0x0, 0x0]]]

"""-------------CLASS DEFINITIONS----------------"""
#this class handles interactions between the code and the physical shift registers
class ShiftRegister():
    def __init__(self, datapin, clockpin, latchpin):
        self.datapin = datapin
        self.clockpin = clockpin
        self.latchpin = latchpin

    def clock(self, n):
        #input data
        GPIO.output(self.datapin, n)
        
        #clock clock (whee)
        GPIO.output(self.clockpin, 1)
        GPIO.output(self.clockpin, 0)
        
        #reset data pin
        GPIO.output(self.datapin, 0)

    def latch(self):
        #latch and reset register
        GPIO.output(self.latchpin, 1)
        GPIO.output(self.latchpin, 0)

    def clear(self):
        #clear and reset register by filling with low values
        for i in range(16):
            self.clock(0)
        self.latch()

#this class runs in a separate thread, continuously reading the 'points' list
#   and writing its values to the LED cube
class Multiplexer():
    def __init__(self):
        self.running = True
        self.register = ShiftRegister(19, 23, 24)

    #the second parameter has to exist for the thread to run, but does nothing
    def multiplex(self, p):
        layer = 0x0
        while self.running:
            for bam_cycle in range(16):
                for led in range(len(points)):
                    self.update_layer(layer)
                    #turn previous layer off before updating LEDs
                    GPIO.output(transistors[y-1], 0)
                    #pick which register to write to - each controls half
                    #   of the cube
                    self.register2.clock(points[y][x][z])
                    #write register values to cube and enable layer
                    self.register1.latch()
                    layer += 1
                    sleep(0.001)
                layer = 0x0

    def update_layer(self, layer):
        for transistor_index in range(len(transistors)):
            mask = 1 << transistor_index
            transistor_bit = (layer & mask) >> transistor_index
            GPIO.output(transistors[transistor_index], transistor_bit)
