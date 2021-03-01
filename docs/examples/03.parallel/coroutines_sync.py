#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time

def c1():
    print("c1-0")
    time.sleep(0.5)
    yield "a"
    print("c1-1")
    time.sleep(0.5)
    yield "b"
    print("c1-2")
    time.sleep(0.5)
    yield "c"
    print("c1-3")

def c2():
    for n in range(3):
        print("c2-%d" % (n))
        time.sleep(0.5)
        yield n
    print("c2-3")

def test2coroutines1():
    r1 = c1()
    r2 = c2()
    for i in range(3):
        print("R1:", next(r1), "R2:", next(r2))

def test2coroutines2():
    for e1, e2 in zip(c1(), c2()):
        print("R1:", e1, "R2:", e2)

if __name__=='__main__':
    test2coroutines1()
    test2coroutines2()
