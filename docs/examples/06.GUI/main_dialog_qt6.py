#!/usr/bin/env python3

# pip install pyqt6 pyqt6_tools

import os
import sys

from PyQt6 import QtWidgets, uic

_scriptdir = os.path.dirname(os.path.realpath(__file__))
uifile = os.path.join(_scriptdir, 'ui', 'main_dialog.ui')

class MainDialog(*uic.loadUiType(uifile)):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.bindEvents()

    def bindEvents(self):
        self.okButton.clicked.connect(self.close)
        self.helloButton.clicked.connect(self.hello)

    def hello(self):
        self.helloLabel.setText(
            "Привет" + ("!" if self.excCheckBox.isChecked() else "")
        )


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    w = MainDialog()
    w.show()

    sys.exit(app.exec())
