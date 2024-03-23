#!/usr/bin/env python3

# pip install pyside6

import os
import sys

from PySide6 import QtWidgets
from PySide6.QtUiTools import loadUiType

_scriptdir = os.path.dirname(os.path.realpath(__file__))
uifile = os.path.join(_scriptdir, 'ui', 'main_dialog.ui')

class MainDialog(*loadUiType(uifile)):
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
