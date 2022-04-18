#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
import multiprocessing

def n_randoms(n):
    s = 123
    m = 2**16+1
    a = 75
    c = 74
    for i in range(n):
        s = (a*s + c) % m

    return s


def test_all(pool):
    l = pool.map(n_randoms, range(1_000_000, 1_000_000 + 50))
    return l


if __name__ == '__main__':
    pool = multiprocessing.Pool()
    t0 = time.time()
    print(test_all(pool))
    print("Time spent:", time.time() - t0)
else:
    print("__name__:", __name__)
