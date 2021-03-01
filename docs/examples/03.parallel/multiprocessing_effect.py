#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import random
import time
import sys
import multiprocessing


def sum_randoms(n):
    g = random.Random()

    r = 0
    for i in range(n):
        r += g.random()

    return r


def test_all(pool):
    l = pool.map(sum_randoms, [1000000] * 50)
    return l


if __name__ == '__main__':
    pool = multiprocessing.Pool()
    t0 = time.time()
    print(test_all(pool))
    print("Time spent:", time.time() - t0)
else:
    print(__name__)
