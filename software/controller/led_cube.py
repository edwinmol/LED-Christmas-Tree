"""--------IMPORT MODULES AND PATTERNS--------"""
import threading
import traceback

import RPi.GPIO as GPIO

from core import Multiplexer
from patterns.geometric import *
from patterns.plane import *
from patterns.points import *
from patterns.rainy import voxelSend
from sequence import Sequence

"""-----------------SEQUENCES----------------"""

sequence = Sequence([[bounce,       "x",                2],
                     [voxelSend,    "N",                20],
                     [firework,     "N",                3],
                     [snake,        "N",                1],
                     [bounce,       "y",                2],
                     [spiral,       "N",                1],
                     [voxelRand,    "N",                175],
                     [tree,         "N",                1]])

"""---------------MAIN FUNCTION----------------"""
try:
    # setup multiplexer and shift registers
    multiplexer = Multiplexer()
    
    # start multiplexing thread
    print("Starting multiplexer thread...")
    multiplexerThread = threading.Thread(target=multiplexer.multiplex())
    multiplexerThread.daemon = True
    multiplexerThread.start()

    # run sequence
    while True:
        sequence.run(1, 0.075)

    GPIO.cleanup()

except KeyboardInterrupt:
    GPIO.cleanup()

except:
    traceback.print_exc()
    GPIO.cleanup()
