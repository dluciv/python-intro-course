#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import random
import timeit
import sys
import threading


def sum_randoms(n: 'int'):
    g = random.Random()

    r = 0
    for i in range(n):
        r = (r + g.random()) % (sys.maxsize // 2)

    return r

def test_all():
    t = threading.Thread(target=lambda : sum_randoms(100000))
    t.start()
    sum_randoms(100000)
    t.join()

if __name__ == '__main__':
    print(timeit.timeit(test_all, number=40))
