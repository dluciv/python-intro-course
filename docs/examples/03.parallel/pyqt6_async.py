#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import asyncio
import PyQt6.QtWidgets as qw
import asyncqt
from asyncqt import asyncSlot
import aiofiles  # https://pypi.org/project/aiofiles/
import aiohttp


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

        self.goBtn = qw.QPushButton('A Go', self)
        self.goBtn.move(50, 50)
        self.goBtn.clicked.connect(self.performLongOperation)

        self.goFileBtn = qw.QPushButton('A File Go', self)
        self.goFileBtn.move(50, 100)
        self.goFileBtn.clicked.connect(self.performLongFileOperation)

        self.goNetBtn = qw.QPushButton('A Net Go', self)
        self.goNetBtn.move(50, 150)
        self.goNetBtn.clicked.connect(self.performLongNetOperation)

        self.quitBtn = qw.QPushButton('Quit', self)
        self.quitBtn.move(50, 200)
        self.quitBtn.clicked.connect(self.close)


    @asyncSlot(bool)
    async def performLongOperation(self, evt):
        self.goBtn.setEnabled(False)
        print("A Going...")
        for c in range(10):
            print("A", c)
            await asyncio.sleep(1)
        print("A Done.")
        self.goBtn.setEnabled(True)

    @asyncSlot(bool)
    async def performLongFileOperation(self, evt):
        async with aiofiles.open("/etc/passwd", 'rb') as f:  # put your file here
            bts = await f.read()
            print("Got", len(bts), "bytes")


    @asyncSlot(bool)
    async def performLongNetOperation(self, evt):
        async with aiohttp.ClientSession() as session:
            for u in urls:
                r = await session.get(u)
                c = await r.read()
                print("Got", u, "of", len(c), "bytes")


if __name__ == '__main__':
    app = qw.QApplication(sys.argv)
    loop = asyncqt.QEventLoop(app)
    asyncio.set_event_loop(loop)

    w = MainWindow()
    w.show()

    with loop:
        sys.exit(loop.run_forever())
