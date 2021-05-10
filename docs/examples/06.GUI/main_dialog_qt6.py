#!/usr/bin/env python3

# pip install PyQt5Designer

import os
import sys

from PyQt6 import QtWidgets, QtCore, QtGui, uic
from PyQt6.QtCore import pyqtSignal, QThread, QTimer
from PyQt6.QtGui import QCursor, QAction

_scriptdir = os.path.dirname(os.path.realpath(__file__))

class MainDialog(*uic.loadUiType(os.path.join(_scriptdir, 'ui', 'main_dialog.ui'))):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.bindEvents()

    def bindEvents(self):
        self.okButton.clicked.connect(self.close)
        self.helloButton.clicked.connect(self.hello)

    def hello(self):
        self.helloLabel.setText("Привет")


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    w = MainDialog()
    w.show()

    sys.exit(app.exec())
