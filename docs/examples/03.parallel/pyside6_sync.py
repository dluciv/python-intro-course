#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import PySide6.QtWidgets as qw
import time

import requests

urls = [
    "https://google.com/",
    "https://yandex.ru/",
    "http://dluciv.name/",
    "https://edu.dluciv.name/",
    "https://spbau.ru/",
    "https://spbu.ru/",
    "https://mail.ru/",
    "http://mil.ru/",
    "https://github.com/"
]


class MainWindow(qw.QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.resize(250, 250)
        self.move(300, 300)
        self.setWindowTitle('Sync')

        self.goBtn = qw.QPushButton('Go', self)
        self.goBtn.move(50, 50)
        self.goBtn.clicked.connect(self.performLongOperation)

        self.goFileBtn = qw.QPushButton('File Go', self)
        self.goFileBtn.move(50, 100)
        self.goFileBtn.clicked.connect(self.performLongFileOperation)

        self.goNetBtn = qw.QPushButton('Net Go', self)
        self.goNetBtn.move(50, 150)
        self.goNetBtn.clicked.connect(self.performLongNetOperation)

        self.quitBtn = qw.QPushButton('Quit', self)
        self.quitBtn.move(50, 200)
        self.quitBtn.clicked.connect(self.close)

    def performLongOperation(self, evt):
        print("Going...")
        for c in range(10):
            print(c)
            time.sleep(1)
        print("Done.")

    def performLongFileOperation(self, evt):
        with open("/etc/passwd", 'rb') as f:
            bts = f.read()
            print("Got", len(bts), "bytes")


    def performLongNetOperation(self, evt):
        for u in urls:
            try:
                r = requests.get(u)
                print("Got", u, "of", len(r.content), "bytes")
            except Exception as e:
                print(f"Error while getting {u}: {e}")


if __name__ == '__main__':
    app = qw.QApplication(sys.argv)
    w = MainWindow()
    w.show()

    sys.exit(app.exec())
