import queue
import threading

import cv2

from systeminputs import isysteminput
from systemoutputs import isystemoutput

from models import response, request


class DetectBall(isysteminput.ISystemInput, threading.Thread):
    def __init__(self, system_output: isystemoutput.ISystemOutput, max_buffering=128):

        # Thread config

        threading.Thread.__init__(self)
        self.daemon = True

        # Usecase Config

        self.system_output = system_output
        self.command_buffer = queue.Queue(maxsize=max_buffering)

    def execute(self, request_model: request.Request):

        # given an frame, calculates the centroid of the pink ball

        if not self.command_buffer.full():
            self.command_buffer.put(request_model)

    def run(self):
        se = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (15, 15))

        while True:

            # This may need to be changed to drain the buffer and always
            # use the latest frame
            while self.command_buffer.qsize() > 1:
                self.command_buffer.get()

            if not self.command_buffer.empty():
                frame = self.command_buffer.get().contents['Frame']
                frame_rows, frame_cols, channels = frame.shape

                hsv = cv2.cvtColor(cv2.GaussianBlur(frame, (5, 5), 2), cv2.COLOR_BGR2HSV)
                _, pink = cv2.threshold(hsv[:, :, 0], 160, 255, cv2.THRESH_BINARY)
                resulting_segmentation = cv2.morphologyEx(pink, cv2.MORPH_OPEN, se)
                moments = cv2.moments(resulting_segmentation)

                if moments["m00"] != 0:
                    cx = int(moments["m10"] / moments["m00"])
                    cy = int(moments["m01"] / moments["m00"])
                else:
                    cx, cy = 0, 0

                # Algorithm implementation here

                # End algorithm implementation

                response_model = response.Response(
                    {
                        'Centroid': (cx, cy),
                        'Frame': frame,
                        'HSV': hsv,
                        'Segmentation': resulting_segmentation,
                        'Frame Width': frame_cols,
                        'Frame Height': frame_rows
                    }
                )
                self.system_output.present(response_model)
