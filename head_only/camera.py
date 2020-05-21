import asyncio
import time
import io
import threading
import picamera
import argparse
import base64
import hashlib
import os
import time
import threading
import webbrowser
import cv2
import numpy as np
from PIL import Image
# from arminit import MoveArm
from xmas import light_up_xmas
import threading
import os
from light_up import light_up

import paho.mqtt.client as paho

broker = "localhost"
port = 1883


def on_publish(client, userdata, result):
    print("data published \n")
    pass


client1 = paho.Client("motors")
client1.on_publish = on_publish
client1.connect(broker, port)


import sys

# from arm import Arm
# from arm.arm_directions import ArmDirections
# from arm.move_arm import move_arm


# default_arm_positions = [np.pi/2, np.pi/2, 0]

## create the robot arm
# arm = Arm.Arm3Link(q=default_arm_positions, L=np.array([90, 60, 48]))

# from motors import move_forward
# sys.path.append('/usr/local/lib/python3.5/dist-packages')


# from nanpy import (ArduinoApi, SerialManager)
#
# connection = SerialManager()
# a = ArduinoApi(connection=connection)
# a.pinMode(11, a.OUTPUT)
# a.pinMode(10, a.OUTPUT)


# Load the model
net = cv2.dnn.readNet(os.path.dirname(__file__) + '/face-detection-adas-0001.xml',
                      os.path.dirname(__file__) + '/face-detection-adas-0001.bin')
# net = cv2.dnn.readNet(os.path.dirname(__file__) + '/pedestrian-detection-adas-0002.xml', os.path.dirname(__file__) + '/pedestrian-detection-adas-0002.bin')
# net = cv2.dnn.readNet(os.path.dirname(__file__) + '/text-detection-0002.xml', os.path.dirname(__file__) + '/text-detection-0002.bin')

# Specify target device
net.setPreferableTarget(cv2.dnn.DNN_TARGET_MYRIAD)


# t = threading.Thread(target=light_up_xmas)
# t.daemon = True


state = {
    'message_sent': False
}


class Camera(object):
    thread = None  # background thread that reads frames from camera
    frame = None  # current frame is stored here by background thread
    last_access = 0  # time of last client access to the camera

    def initialize(self):
        if Camera.thread is None:
            # start background frame thread
            Camera.thread = threading.Thread(target=self._thread)
            Camera.thread.start()

            # wait until frames start to be available
            while self.frame is None:
                time.sleep(0)

    def get_frame(self):
        Camera.last_access = time.time()
        self.initialize()
        return self.frame

    @classmethod
    def _thread(cls):
        with picamera.PiCamera() as camera:
            # camera setup
            camera.resolution = (320, 240)
            camera.framerate = 32
            camera.hflip = True
            camera.vflip = True

            # let camera warm up
            camera.start_preview()
            time.sleep(2)

            stream = io.BytesIO()

            for foo in camera.capture_continuous(stream, 'jpeg',
                                                 use_video_port=True):

                ####################

                # frame = camera.capture(sio, "jpeg", use_video_port=True)
                data = np.fromstring(stream.getvalue(), dtype=np.uint8)

                image = cv2.imdecode(data, 1)

                # Prepare input blob and perform an inference
                blob = cv2.dnn.blobFromImage(image, size=(672, 384), ddepth=cv2.CV_8U)
                net.setInput(blob)
                out = net.forward()

                # Draw detected faces on the frame
                for detection in out.reshape(-1, 7):
                    confidence = float(detection[2])
                    xmin = int(detection[3] * image.shape[1])
                    ymin = int(detection[4] * image.shape[0])
                    xmax = int(detection[5] * image.shape[1])
                    ymax = int(detection[6] * image.shape[0])

                    if confidence > 0.5:
                        # asyncio.run(light_up_xmas())
                        # a.digitalWrite(11, a.HIGH)
                        # a.digitalWrite(10, a.HIGH)
                        light_up()
                        cv2.rectangle(image, (xmin, ymin), (xmax, ymax), color=(0, 255, 0))
                        print('the geometry is: x, y')
                        print(xmax - xmin)
                        print(ymax - ymin)
                        if not state['message_sent']:
                            ret = client1.publish("pi/wheels", "on")
                            state['message_sent'] = True
                            print('on')

                        # old_angles = default_arm_positions
                        #
                        # # x, y = -100, 80
                        #
                        # x, y = -70, 0
                        #
                        # arm.q = arm.inv_kin([2180/(ymax - ymin), 0])
                        #
                        # new_angles = arm.q
                        #
                        # move_arm(old_angles[0] - new_angles[0], ArmDirections.up(), ArmDirections.down())
                        # move_arm(old_angles[1] - new_angles[1], ArmDirections.elbow_up(), ArmDirections.elbow_down())
                        # move_arm(old_angles[2] - new_angles[2], ArmDirections.wrist_up(), ArmDirections.wrist_down())
                        #
                        # move_arm(old_angles[0] - new_angles[0], ArmDirections.down(), ArmDirections.up())
                        # move_arm(old_angles[1] - new_angles[1], ArmDirections.elbow_down(), ArmDirections.elbow_up())
                        # move_arm(old_angles[2] - new_angles[2], ArmDirections.wrist_down(), ArmDirections.wrist_up())

                        # move_forward()
                    else:
                        if state['message_sent']:
                            ret = client1.publish("pi/wheels", "off")
                            state['message_sent'] = False
                            print('off')
                        # a.digitalWrite(11, a.LOW)
                        # a.digitalWrite(10, a.LOW)

                ret, jpeg = cv2.imencode('.jpg', image)
                testbytes = jpeg.tobytes()

                ####################

                # store frame
                stream.seek(0)
                cls.frame = testbytes
                # cls.frame = stream.read()

                # reset stream for next frame
                stream.seek(0)
                stream.truncate()

                # if there hasn't been any clients asking for frames in
                # the last 10 seconds stop the thread
                if time.time() - cls.last_access > 10:
                    break
        cls.thread = None
