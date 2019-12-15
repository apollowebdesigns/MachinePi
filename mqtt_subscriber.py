import paho.mqtt.client as paho
from time import sleep

broker = "localhost"
port = 1883
#
#
# def on_subscribe(client, userdata, result):
#     print("hit \n")
#     pass
#
#
# client1 = paho.Client("motors")
#
# client1.on_subscribe = on_subscribe
#
# client1.connect(broker, port)
# client1.subscribe("pi/wheels", 2)
# client1.loop_forever()

#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright (c) 2010-2013 Roger Light <roger@atchoo.org>
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Eclipse Distribution License v1.0
# which accompanies this distribution.
#
# The Eclipse Distribution License is available at
#   http://www.eclipse.org/org/documents/edl-v10.php.
#
# Contributors:
#    Roger Light - initial implementation
# Copyright (c) 2010,2011 Roger Light <roger@atchoo.org>
# All rights reserved.

# This shows a simple example of an MQTT subscriber.

import paho.mqtt.client as mqtt


def on_connect(mqttc, obj, flags, rc):
    print("rc: " + str(rc))


def on_message(mqttc, obj, msg):
    print(msg.topic + " " + str(msg.qos) + " " + str(msg.payload))


def on_publish(mqttc, obj, mid):
    print("mid: " + str(mid))


def on_subscribe(mqttc, obj, mid, granted_qos):
    print("Subscribed: " + str(mid) + " " + str(granted_qos))


def on_log(mqttc, obj, level, string):
    print(string)


# If you want to use a specific client id, use
# mqttc = mqtt.Client("client-id")
# but note that the client id must be unique on the broker. Leaving the client
# id parameter empty will generate a random id for you.
client1 = mqtt.Client("motors")
client1.on_message = on_message
client1.on_connect = on_connect
client1.on_publish = on_publish
client1.on_subscribe = on_subscribe
# Uncomment to enable debug messages
# mqttc.on_log = on_log
client1.connect(broker, port)
client1.subscribe("$SYS/#", 0)

client1.loop_forever()
