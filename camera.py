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

# Load the model
net = cv2.dnn.readNet('face-detection-adas-0001.xml', 'face-detection-adas-0001.bin')

# Specify target device
net.setPreferableTarget(cv2.dnn.DNN_TARGET_MYRIAD)


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
            camera.hflip = True
            camera.vflip = True

            # let camera warm up
            camera.start_preview()
            time.sleep(2)

            stream = io.BytesIO()

            testbytes = b''

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
                        light_up_xmas()
                        cv2.rectangle(image, (xmin, ymin), (xmax, ymax), color=(0, 255, 0))

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