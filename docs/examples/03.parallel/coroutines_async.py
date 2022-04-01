#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# https://makina-corpus.com/blog/metier/2015/python-http-server-with-the-new-async-await-syntax

import asyncio

@asyncio.coroutine
def c1():
    print("c1-0")
    yield from asyncio.sleep(0.5)
    print("c1-1")
    yield from asyncio.sleep(0.5)
    print("c1-2")
    yield from asyncio.sleep(0.5)
    print("c1-3")


@asyncio.coroutine
def c2():
    for n in range(3):
        yield from asyncio.sleep(0.5)
        print("c2-%d" % (n))
    print("c2-3")


async def c3():
    for n in range(3):
        await asyncio.sleep(0.5)
        print("c3-%d" % (n))
    print("c3-3")

@asyncio.coroutine
def test3coroutines():
    yield from asyncio.wait([
        c1(),
        c2(),
        c3()
    ])


if __name__=='__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(test3coroutines())
