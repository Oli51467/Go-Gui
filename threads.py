# -*- coding: utf-8 -*-
import time

import serial
from PyQt5 import QtCore


class SerialThread(QtCore.QThread):
    def __init__(self, parent=None):
        super(SerialThread, self).__init__(parent)

    # 打开串口
    def port_open(self):
        self.ser = serial.Serial(port="/dev/ttyS1", baudrate=115200)

        try:
            self.ser.open()
        except:
            print('此串口不能被打开')
            return
        if self.ser.isOpen():
            print("串口状态（已开启）")

    def serial_send(self):
        self.ser.write("done".encode('utf-8'))

    def run(self):
        while True:
            com_input = self.ser.read(5)
            if com_input is not None:
                print(com_input)


