#!/usr/bin/env python
import RPi.GPIO as GPIO
import time

IR1 = 7
IR2 = 11
IR3 = 13
IR4 = 15

GPIO.setmode(GPIO.BOARD)       # Set the GPIOS physical location as numbers
GPIO.setup(IR1, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(IR2, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(IR3, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(IR4, GPIO.IN, pull_up_down=GPIO.PUD_UP)

while True:
        print("############")
        print("# {}        #".format(GPIO.input(IR1)))
        print("# {}        #".format(GPIO.input(IR2)))
        print("# {}        #".format(GPIO.input(IR3)))
        print("# {}        #".format(GPIO.input(IR4)))
        print("############")
        print(" ")
        time.sleep(0.2)
        
