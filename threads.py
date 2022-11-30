# -*- coding: utf-8 -*-
from PyQt5 import QtCore

import funcs

games = []


class NetworkThread(QtCore.QThread):
    def __init__(self, parent=None):
        super(NetworkThread, self).__init__(parent)



