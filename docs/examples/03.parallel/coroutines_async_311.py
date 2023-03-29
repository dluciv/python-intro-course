#!/usr/bin/env python3.11

# https://makina-corpus.com/blog/metier/2015/python-http-server-with-the-new-async-await-syntax

# Python >= 3.11

import asyncio

async def c1():
    print("c1-0")
    await asyncio.sleep(1)
    print("c1-1")
    await asyncio.sleep(1)
    print("c1-2")
    await asyncio.sleep(1)
    print("c1-3")

async def c2():
    for n in range(3):
        await asyncio.sleep(1)
        print("c2-%d" % (n))
    print("c2-3")


async def c3():
    for n in range(3):
        await asyncio.sleep(1)
        print("c3-%d" % (n))
    print("c3-3")

async def test3coroutines():
    async with asyncio.TaskGroup() as tg:
        for c in [c1(), c2(), c3()]:
            tg.create_task(c)

if __name__=='__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(test3coroutines())
