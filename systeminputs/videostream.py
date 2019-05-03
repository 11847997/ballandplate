import time
import threading
import cv2

from systeminputs import isysteminput

from models import request
from usecases import detectball


class VideoStream(threading.Thread):
    def __init__(self, usecase: isysteminput.ISystemInput, camera_id=1, fps=60):

        # Thread config

        threading.Thread.__init__(self)
        self.daemon = True

        # Video Stream config

        self.usecase = usecase
        self.webcam = cv2.VideoCapture(camera_id)
        self.fps = fps
        self.webcam.set(cv2.CAP_PROP_FPS, self.fps)
        print('width ', self.webcam.get(cv2.CAP_PROP_FRAME_WIDTH))
        print('height ', self.webcam.get(cv2.CAP_PROP_FRAME_HEIGHT))

        self.webcam.set(cv2.CAP_PROP_FRAME_WIDTH, 352)
        self.webcam.set(cv2.CAP_PROP_FRAME_HEIGHT, 288)

        print('new width ', self.webcam.get(cv2.CAP_PROP_FRAME_WIDTH))
        print('new height ', self.webcam.get(cv2.CAP_PROP_FRAME_HEIGHT))
        # wait to make sure the camera is up and running
        print(self.webcam.get(cv2.CAP_PROP_FPS))

        time.sleep(2)

        if not self.webcam.isOpened():
            raise ConnectionError('Failed to connect to camera')

    def run(self):
        while True:

            # The read method is extremely slow due to opencv internal buffering, it is a known issue.
            # The current workaround without using C++

            self.webcam.grab()
            grabbed, frame = self.webcam.retrieve(0)  # self.webcam.read()#
            if grabbed:
                request_model = request.Request({'Frame': frame})
                self.usecase.execute(request_model)
            # time.sleep(1 / self.fps)

    def __del__(self):
        self.webcam.release()
