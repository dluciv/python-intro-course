#!/usr/bin/env python3

# pip install pyqt6 pyqt6_tools

from functools import partial
import os
import sys

from PyQt6 import QtWidgets, uic
from PyQt6.QtCore import pyqtBoundSignal

_scriptdir = os.path.dirname(os.path.realpath(__file__))
uifile = os.path.join(_scriptdir, 'ui', 'main_dialog.ui')

class AutoBindingWidget:
    def autoBindEvents(self):
        for wn, w in self.__dict__.items():
            match type(w):
                case QtWidgets.QPushButton:  # Сделать для любого Виджета
                    # И поискать события в w.__dir__()
                    clh = type(self).__dict__.get(wn + '_clicked')
                    if clh:
                        print(type(w.clicked))  # <class 'PyQt6.QtCore.pyqtBoundSignal'> # И для всех сигналов
                        w.clicked.connect(partial(clh, self))

class MainDialog(*uic.loadUiType(uifile), AutoBindingWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.autoBindEvents()

    def okButton_clicked(self):
        self.close()

    def helloButton_clicked(self):
        self.helloLabel.setText(
            "Привет" + ("!" if self.excCheckBox.isChecked() else "")
        )


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    w = MainDialog()
    w.show()

    sys.exit(app.exec())
