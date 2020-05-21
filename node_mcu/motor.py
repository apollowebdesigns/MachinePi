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



from time import sleep
from nanpy import SerialManager, ArduinoApi

connection_three = SerialManager(device='/dev/ttyUSB2')
a_three = ArduinoApi(connection=connection_three)

leftForward = 13
leftBackward = 15
rightForward = 4
rightBackward = 5


a_three.pinMode(leftForward, a_three.OUTPUT)
a_three.pinMode(leftBackward, a_three.OUTPUT)
a_three.pinMode(rightForward, a_three.OUTPUT)
a_three.pinMode(rightBackward, a_three.OUTPUT)

while True:
    print('on')
    a_three.digitalWrite(leftForward, a_three.HIGH)
    a_three.digitalWrite(leftBackward, a_three.LOW)
    a_three.digitalWrite(rightForward, a_three.HIGH)
    a_three.digitalWrite(rightBackward, a_three.LOW)
    sleep(2)
    print('off')
    a_three.digitalWrite(leftForward, a_three.LOW)
    a_three.digitalWrite(leftBackward, a_three.LOW)
    a_three.digitalWrite(rightForward, a_three.LOW)
    a_three.digitalWrite(rightBackward, a_three.LOW)