from sense_hat import SenseHat
from random import randint
from time import sleep

sense = SenseHat()


def light_up():
    x = randint(0, 7)
    y = randint(0, 7)
    r = randint(0, 255)
    g = randint(0, 255)
    b = randint(0, 255)
    sense.set_pixel(x, y, r, g, b)
    sleep(2)


def clear():
    sense.clear()
