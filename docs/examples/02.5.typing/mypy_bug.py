#!/usr/bin/env python3

from numbers import Number

# MyPy считает, что int — не Number https://github.com/python/mypy/issues/3186

def handle_simple(i: Number) -> None:
    print(str(i) + "abc")

handle_simple(123)
