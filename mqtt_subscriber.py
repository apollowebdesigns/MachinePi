import paho.mqtt.client as paho
from time import sleep

broker = "localhost"
port = 1883


def on_subscribe(client, userdata, result):
    print("hit \n")
    pass


client1 = paho.Client("motors")

client1.on_subscribe = on_subscribe

client1.connect(broker, port)
client1.subscribe("pi/wheels", 2)
client1.loop_forever()
