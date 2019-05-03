import serial
from systemoutputs import isystemoutput
from models import view, response

from serial.tools import list_ports

class USBOutput(isystemoutput.ISystemOutput):
    def __init__(self, view: view.View):
        self.view = view

        self.baudrate = 115200
        #tty.usbserial-FTE30K1U
        self.device_id = '/dev/cu.usbserial-FTE30K1U'
        #self.device_id = '/dev/ttyUSB0'
        self.ser = serial.Serial(self.device_id, self.baudrate)

        # any initialisation for the usb goes here

        # end usb initialisation

    def present(self, reponse_model: response.Response):
        # Write the code to output to usb here

        # print('Centroid', reponse_model.contents['Centroid'])
        Xstr = (format(int(reponse_model.contents['Centroid'][0]), '04d'))
        Ystr = (format(int(reponse_model.contents['Centroid'][1]), '04d'))
        str_out = '<0,1,' + Xstr + ',' + Ystr + '>\r\n'
        self.ser.write(str_out.encode())

        # Anything that needs to be displayed on the video feed can be placed into the view contents dto

        self.view.contents['Frame'] = reponse_model.contents['Frame']
        self.view.contents['HSV'] = reponse_model.contents['HSV']
        self.view.contents['Segmentation'] = reponse_model.contents['Segmentation']
        self.view.contents['Centroid'] = reponse_model.contents['Centroid']
        self.view.contents['Frame Width'] = reponse_model.contents['Frame Width']
        self.view.contents['Frame Height'] = reponse_model.contents['Frame Height']
