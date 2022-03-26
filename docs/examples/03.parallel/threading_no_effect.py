#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import timeit
import threading


def n_randoms(n):
    s = 123
    m = 2**16+1
    a = 75
    c = 74
    for i in range(n):
        s = (a*s + c) % m

    return s

def test_all():
    t = threading.Thread(target=lambda : n_randoms(10000000))
    t.start()
    # n_randoms(10000000)
    n_randoms(10000000)
    t.join()

if __name__ == '__main__':
    print(timeit.timeit(test_all, number=1))
