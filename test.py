import io
import os
import picamera
import cv2
import logging
import socketserver
from threading import Condition
from http import server
import numpy as np

PAGE="""\
<html>
<head>
<title>picamera MJPEG streaming demo</title>
</head>
<body>
<h1>PiCamera MJPEG Streaming Demo</h1>
<img src="stream.mjpg" width="640" height="480" />
</body>
</html>
"""

directory_path = os.path.dirname(__file__)
if directory_path != '':
    directory_path = '/'

# Load the model
net = cv2.dnn.readNet(directory_path + 'face-detection-adas-0001.xml', directory_path + 'face-detection-adas-0001.bin')

# Specify target device
net.setPreferableTarget(cv2.dnn.DNN_TARGET_MYRIAD)


class StreamingOutput(object):
    def __init__(self):
        self.frame = None
        self.buffer = io.BytesIO()
        self.condition = Condition()

    def open_cv_process_image(self, frame):
        print('hit22')
        data = np.fromstring(frame, dtype=np.uint8)
        print('hit1')
        if frame.empty():
            print('empty')
            return frame
        image = cv2.imdecode(data, 1)
        print('hit2')
        blob = cv2.dnn.blobFromImage(image, size=(672, 384), ddepth=cv2.CV_8U)
        print('hit3')
        net.setInput(blob)
        print('hit4')
        out = net.forward()

        # Draw detected faces on the frame
        for detection in out.reshape(-1, 7):
            confidence = float(detection[2])
            xmin = int(detection[3] * image.shape[1])
            ymin = int(detection[4] * image.shape[0])
            xmax = int(detection[5] * image.shape[1])
            ymax = int(detection[6] * image.shape[0])
            if confidence > 0.5:
                cv2.rectangle(image, (xmin, ymin), (xmax, ymax), color=(0, 255, 0))

        ret, jpeg = cv2.imencode('.mjpg', image)
        testbytes = jpeg.tobytes()
        return jpeg

    def write(self, buf):
        if buf.startswith(b'\xff\xd8'):
            print('hit')
            # New frame, copy the existing buffer's content and notify all
            # clients it's available
            self.buffer.truncate()
            with self.condition:
                # self.frame = self.buffer.getvalue()
                self.frame = self.open_cv_process_image(self.buffer)
                self.condition.notify_all()
            self.buffer.seek(0)
        else:
            print('old frame')
        return self.buffer.write(buf)

class StreamingHandler(server.BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(301)
            self.send_header('Location', '/index.html')
            self.end_headers()
        elif self.path == '/index.html':
            content = PAGE.encode('utf-8')
            self.send_response(200)
            self.send_header('Content-Type', 'text/html')
            self.send_header('Content-Length', len(content))
            self.end_headers()
            self.wfile.write(content)
        elif self.path == '/stream.mjpg':
            self.send_response(200)
            self.send_header('Age', 0)
            self.send_header('Cache-Control', 'no-cache, private')
            self.send_header('Pragma', 'no-cache')
            self.send_header('Content-Type', 'multipart/x-mixed-replace; boundary=FRAME')
            self.end_headers()
            try:
                while True:
                    with output.condition:
                        output.condition.wait()
                        frame = output.frame
                    self.wfile.write(b'--FRAME\r\n')
                    self.send_header('Content-Type', 'image/jpeg')
                    self.send_header('Content-Length', len(frame))
                    self.end_headers()
                    self.wfile.write(frame)
                    self.wfile.write(b'\r\n')
            except Exception as e:
                logging.warning(
                    'Removed streaming client %s: %s',
                    self.client_address, str(e))
        else:
            self.send_error(404)
            self.end_headers()

class StreamingServer(socketserver.ThreadingMixIn, server.HTTPServer):
    allow_reuse_address = True
    daemon_threads = True

with picamera.PiCamera(resolution='640x480', framerate=24) as camera:
    output = StreamingOutput()
    camera.start_recording(output, format='mjpeg')
    try:
        address = ('', 8000)
        server = StreamingServer(address, StreamingHandler)
        server.serve_forever()
    finally:
        camera.stop_recording()