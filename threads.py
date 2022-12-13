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
        if self.ser.isOpen():
            print('串口已开启')
            return True
        else:
            try:
                self.ser.open()
            except:
                print('此串口不能被打开')
                return False
            if self.ser.isOpen():
                print("串口状态（已开启）")
                return True

    def serial_send(self):
        self.ser.write("done".encode('utf-8'))

    def run(self):
        while True:
            try:
                num = self.ser.inWaiting()
            except:
                self.port_close()
                return None
            if num > 0:
                com_input = self.ser.read(num)
                print(com_input.decode('utf-8'))


