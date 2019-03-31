from systemoutputs import isystemoutput
from models import view, response


class USBOutput(isystemoutput.ISystemOutput):
    def __init__(self, view: view.View):
        self.view = view

        # any initialisation for the usb goes here

        # end usb initialisation

    def present(self, reponse_model: response.Response):
        # Write the code to output to usb here

        print('Centroid', reponse_model.contents['Centroid'])

        # Anything that needs to be displayed on the video feed can be placed into the view contents dto

        self.view.contents['Frame'] = reponse_model.contents['Frame']
        self.view.contents['Centroid'] = reponse_model.contents['Centroid']
