"""--------IMPORT MODULES AND PATTERNS--------"""
import threading
import traceback
import RPi.GPIO as GPIO
from core import Multiplexer
from patterns.plot import *
from patterns.geometric import *
from patterns.plane import *
from time import sleep
from sequence import Sequence

"""-----------------SEQUENCES----------------"""

sequence = Sequence([[bounce,      "x",                2],
                     [bounce,      "y",                2],
                     [spiral,      "N",                6]])

"""---------------MAIN FUNCTION----------------"""
try:
    #setup multiplexer and shift registers
    multiplexer = Multiplexer()
    
    #start multiplexing thread
    print("Starting multiplexer thread...")
    multiplexerThread = threading.Thread(target=multiplexer.multiplex())
    multiplexerThread.daemon=True
    multiplexerThread.start()

    #run sequence
    sequence.run(1, 0.075)

    GPIO.cleanup()

except KeyboardInterrupt:
    GPIO.cleanup()

except:
    traceback.print_exc()
    GPIO.cleanup()
