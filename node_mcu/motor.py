from time import sleep
from nanpy import SerialManager, ArduinoApi

connection_one = SerialManager(device='/dev/ttyUSB0')
a_one = ArduinoApi(connection=connection_one)

leftForward = 13
leftBackward = 15
rightForward = 4
rightBackward = 5
a_one.pinMode(leftForward, a_one.OUTPUT)
a_one.pinMode(leftBackward, a_one.OUTPUT)
a_one.pinMode(rightForward, a_one.OUTPUT)
a_one.pinMode(rightBackward, a_one.OUTPUT)


while True:
    a_one.digitalWrite(leftForward, a_one.HIGH)
    a_one.digitalWrite(leftBackward, a_one.LOW)
    a_one.digitalWrite(rightForward, a_one.HIGH)
    a_one.digitalWrite(rightBackward, a_one.LOW)
    sleep(2)
    a_one.digitalWrite(leftForward, a_one.LOW)
    a_one.digitalWrite(leftBackward, a_one.LOW)
    a_one.digitalWrite(rightForward, a_one.LOW)
    a_one.digitalWrite(rightBackward, a_one.LOW)
    sleep(2)
