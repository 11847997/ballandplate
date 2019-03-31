import queue
import threading

from models import response, request
from systemoutputs import consoleprinter


class DetectBall(threading.Thread):
    def __init__(self, system_output: consoleprinter.ConsolePrinter, max_buffering=128):

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
        while True:

            # This may need to be changed to drain the buffer and always
            # use the latest frame

            if not self.command_buffer.empty():
                frame = self.command_buffer.get().contents['Frame']


                # Algorithm implementation here


                # End algorithm implementation

                response_model = response.Response(
                    {
                        'Centroid': (frame[1, 2, 0], frame[2, 3, 0]),
                        'Frame': frame
                    }
                )
                self.system_output.present(response_model)

