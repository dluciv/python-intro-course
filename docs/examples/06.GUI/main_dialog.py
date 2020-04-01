#!/usr/bin/env python3
import os
import sys

from PyQt5 import QtWidgets, QtCore, QtGui, uic
from PyQt5.QtCore import pyqtSignal, QThread, QTimer
from PyQt5.QtGui import QCursor
from PyQt5.QtWebChannel import QWebChannel
from PyQt5.QtWidgets import QAction

_scriptdir = os.path.dirname(os.path.realpath(__file__))

class MainDialog(*uic.loadUiType(os.path.join(_scriptdir, 'ui', 'main_dialog.ui'))):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.bindEvents()

    def bindEvents(self):
        self.okButton.clicked.connect(self.close)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    w = MainDialog()
    w.show()

    sys.exit(app.exec_())
