from gpiozero import LEDBoard
from gpiozero.tools import random_values
from time import sleep
tree = LEDBoard(*range(2,28),pwm=True)


def light_up_xmas():
    for led in tree:
        led.source_delay = 0.1
        led.source = random_values()
