#!/usr/bin/env python3

import os

from PyQt5 import QtWidgets, QtCore, QtGui, uic
from PyQt5.QtCore import pyqtSignal, QThread, QTimer
from PyQt5.QtGui import QCursor
from PyQt5.QtWebChannel import QWebChannel
from PyQt5.QtWidgets import QAction

_scriptdir = os.path.dirname(os.path.realpath(__file__))
_scriptname = os.path.basename(os.path.realpath(__file__))

class MainDialog(QtWidgets.QDialog, uic.loadUiType(os.path.join('ui', 'main_dialog.ui'))):
    def __init__(self, parent=None):
        QtWidgets.QDialog.__init__(self, parent)
        self.setupUi(self)
        self.setFixedSize(self.size())
        self.bindEvents()

    def bindEvents(self):
        self.okButton.connect(self.close)

if __name__ == '__main__':
    app = qw.QApplication(sys.argv)
    w = MainDialog()
    w.show()

    sys.exit(app.exec_())
