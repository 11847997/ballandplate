import cv2

from models import view

from systeminputs import videostream
from systemoutputs import usboutput
from usecases import detectball


def main():

    # The view_model controls what is displayed in the video feed
    # System outputs know of this and can modify.

    view_model = view.View(
        {
            'Frame': None,

            # Tracking properties
            'Centroid': (0, 0),
            'Draw Radius': 50,
            'Draw Color': (255, 255, 255),
            'Line Thickness': 2,

            # Text Properties
            'Font': cv2.FONT_HERSHEY_SIMPLEX,
            'Text Placement': (10, 500),  # bottom left corner of text (x, y)
            'Font Scale': 1,
            'Font Color': (175, 138, 192),
            'Font Line Thickness': 2
        }
    )

    # The input, output, and algorithm of the system can be configured here, if you want to write
    # to a different output device, you need to write a new presenter

    console_presenter = usboutput.USBOutput(view_model)
    detection_algorithm = detectball.DetectBall(console_presenter)
    input_stream = videostream.VideoStream(detection_algorithm, fps=30)

    # Start the needed components in order, All threads are daemons and will commit suicide on exit. This
    # is fine because we are not doing any critical operations

    detection_algorithm.start()
    input_stream.start()

    # Show the results to the user here

    while True:
        if view_model.contents['Frame'] is not None:

            # Draw tracking circle on screen

            cv2.circle(
                view_model.contents['Frame'],
                view_model.contents['Centroid'],
                view_model.contents['Draw Radius'],
                view_model.contents['Draw Color'],
                thickness=view_model.contents['Line Thickness']
            )

            # Draw centroid text on screen

            cv2.putText(
                view_model.contents['Frame'],
                str(view_model.contents['Centroid']),
                view_model.contents['Text Placement'],
                view_model.contents['Font'],
                view_model.contents['Font Scale'],
                view_model.contents['Font Color'],
                view_model.contents['Font Line Thickness']
            )

            cv2.imshow('Frame', view_model.contents['Frame'])

        if cv2.waitKey(1) & 0xFF == ord('q'):
            print('Terminating Application')
            break

    # Clean up

    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
