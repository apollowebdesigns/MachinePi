import RPi.GPIO as GPIO
from time import sleep

from nanpy import (ArduinoApi, SerialManager)


connection = SerialManager()
a = ArduinoApi(connection=connection)


def move_forward():
    leftForward = 2
    leftBackward = 3
    rightForward = 4
    rightBackward = 5
    a.pinMode(leftForward, a.OUTPUT)
    a.pinMode(leftBackward, a.OUTPUT)
    a.pinMode(rightForward, a.OUTPUT)
    a.pinMode(rightBackward, a.OUTPUT)

    a.digitalWrite(leftForward, a.HIGH)
    a.digitalWrite(leftBackward, a.LOW)
    a.digitalWrite(rightForward, a.HIGH)
    a.digitalWrite(rightBackward, a.LOW)

    sleep(1)

    a.digitalWrite(leftForward, a.LOW)
    a.digitalWrite(leftBackward, a.LOW)
    a.digitalWrite(rightForward, a.LOW)
    a.digitalWrite(rightBackward, a.LOW)
