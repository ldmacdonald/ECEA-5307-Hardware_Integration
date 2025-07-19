# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

import time

import board
import digitalio

import adafruit_matrixkeypad

import requests
import RPi.GPIO as GPIO

def check_product(product):
    
    try:
        request_body = "http://192.168.254.181:5000/identity/{}".format(str(product))
        response = requests.get(request_body)
        data = response.json()
        print(data)
        return True
    except requests.exceptions.JSONDecodeError:
        print("Response is not in JSON format")
    except requests.exceptions.RequestException:
        print("Likely connection issue")
    
    return False

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
lcd.write_string("Welcome")

#GPIO.setmode(GPIO.BOARD)
GPIO.setup(25, GPIO.OUT)

product = ""

while True:
    keys = keypad.pressed_keys
    if keys:
        if len(keys) == 1:
            print("Pressed: ", str(keys[0]))
            if len(product) < 2:
                product = product + str(keys[0])
            else:
                product = str(keys[0])
        message = "Keys Pressed: {}".format(str(product))
        lcd.clear()
        lcd.write_string(message)
        time.sleep(1.0)
        lcd.clear()
        print(len(product))
        
        if len(product) > 1:
            print("checking")
            check_message = "Checking: {}".format(str(product))
            lcd.write_string(check_message)
            if check_product(product):
                lcd.clear()
                lcd.write_string('Dispensing')
                # Structure for driving 'motor'
                GPIO.output(25, GPIO.HIGH)
                time.sleep(1.0)
                GPIO.output(25, GPIO.LOW)
                lcd.clear()
                lcd.write_string("Welcome")
            else:
                lcd.clear()
                fail_message = "Unable to Dispense: {}".format(str(product))
                lcd.write_string(fail_message)
                time.sleep(0.5)
                lcd.clear()
                lcd.write_string("Welcome")
    time.sleep(0.1)
GPIO.cleanup()
