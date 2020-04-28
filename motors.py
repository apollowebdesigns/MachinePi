import RPi.GPIO as GPIO
from time import sleep

from nanpy import (ArduinoApi, SerialManager)


connection = SerialManager()
a = ArduinoApi(connection=connection)

class Motor:
    """
    Motor class to work with a pair of motors for nodemcu pins.

    Pins are currently fixed in this position, but could be altered at a later stage.
    """
    def __init__(self):
        self.leftForward = 2
        self.leftBackward = 3
        self.rightForward = 4
        self.rightBackward = 5
        a.pinMode(self.leftForward, a.OUTPUT)
        a.pinMode(self.leftBackward, a.OUTPUT)
        a.pinMode(self.rightForward, a.OUTPUT)
        a.pinMode(self.rightBackward, a.OUTPUT)

    def forward(self, duration=1):
        a.digitalWrite(self.leftForward, a.HIGH)
        a.digitalWrite(self.leftBackward, a.LOW)
        a.digitalWrite(self.rightForward, a.HIGH)
        a.digitalWrite(self.rightBackward, a.LOW)

        sleep(duration)

        self._set_low_output()

    def backward(self, duration=1):
        a.digitalWrite(self.leftForward, a.LOW)
        a.digitalWrite(self.leftBackward, a.HIGH)
        a.digitalWrite(self.rightForward, a.LOW)
        a.digitalWrite(self.rightBackward, a.HIGH)

        sleep(duration)

        self._set_low_output()

    def left(self, duration=1):
        a.digitalWrite(self.leftForward, a.LOW)
        a.digitalWrite(self.leftBackward, a.HIGH)
        a.digitalWrite(self.rightForward, a.HIGH)
        a.digitalWrite(self.rightBackward, a.LOW)

        sleep(duration)

        self._set_low_output()

    def right(self, duration=1):
        a.digitalWrite(self.leftForward, a.HIGH)
        a.digitalWrite(self.leftBackward, a.LOW)
        a.digitalWrite(self.rightForward, a.LOW)
        a.digitalWrite(self.rightBackward, a.HIGH)

        sleep(duration)

        self._set_low_output()

    def _set_low_output(self):
        a.digitalWrite(self.leftForward, a.LOW)
        a.digitalWrite(self.leftBackward, a.LOW)
        a.digitalWrite(self.rightForward, a.LOW)
        a.digitalWrite(self.rightBackward, a.LOW)

