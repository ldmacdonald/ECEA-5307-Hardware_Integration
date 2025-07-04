# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

import time

import board
import digitalio

import adafruit_matrixkeypad

# LCD Setup
from RPLCD.i2c import CharLCD
lcd = CharLCD('PCF8574', 0x27)

print("Starting")

# Membrane 3x4 matrix keypad on Raspberry Pi -
# https://www.adafruit.com/product/419
cols = [digitalio.DigitalInOut(x) for x in (board.D26, board.D20, board.D21)]
rows = [digitalio.DigitalInOut(x) for x in (board.D5, board.D6, board.D13, board.D19)]

# 3x4 matrix keypad on Raspberry Pi -
# rows and columns are mixed up for https://www.adafruit.com/product/3845
# cols = [digitalio.DigitalInOut(x) for x in (board.D26, board.D20, board.D21)]
# rows = [digitalio.DigitalInOut(x) for x in (board.D5, board.D6, board.D13, board.D19)]

keys = ((1, 2, 3), (4, 5, 6), (7, 8, 9), ("*", 0, "#"))

keypad = adafruit_matrixkeypad.Matrix_Keypad(rows, cols, keys)

# I2C
lcd.write_string("Starting")

GPIO.setmode(GPIO.BOARD)
GPIO.setup(25, GPIO.OUT)

while True:
    keys = keypad.pressed_keys
    if keys:
        print("Pressed: ", keys)
        message = "Pressed: {}\n".format(str(keys))
        lcd.clear()
        lcd.write_string(message)
        # Structure for driving 'motor'
        # GPIO.output(25, GPIO.HIGH)
        # time.sleep(1)
        # GPIO.output(25, GPIO.LOW)
    time.sleep(0.1)
#GPIO.cleanup()
