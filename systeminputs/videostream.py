import time
import threading
import cv2

from models import request
from usecases import detectball


class VideoStream(threading.Thread):
    def __init__(self, usecase: detectball.DetectBall, camera_id=0, fps=60):

        # Thread config

        threading.Thread.__init__(self)
        self.daemon = True

        # Video Stream config

        self.usecase = usecase
        self.webcam = cv2.VideoCapture(camera_id)
        self.fps = fps

        # wait to make sure the camera is up and running

        time.sleep(2)

        if not self.webcam.isOpened():
            raise ConnectionError('Failed to connect to camera')

    def run(self):
        while True:

            # The read method is extremely slow due to opencv internal buffering, it is a known issue.
            # The current workaround without using C++

            self.webcam.grab()
            grabbed, frame = self.webcam.retrieve()
            if grabbed:
                request_model = request.Request({'Frame': frame})
                self.usecase.execute(request_model)
            time.sleep(1 / self.fps)

    def __del__(self):
        self.webcam.release()
