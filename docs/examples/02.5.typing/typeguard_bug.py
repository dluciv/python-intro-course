#!/usr/bin/env python3

from typeguard import typechecked
import typing

@typechecked
def handle_strings_or_ints_py_3_10(values: list[str | int]) -> str:
    return "OK: " + " + ".join(map(str, values))

@typechecked
def handle_strings_or_ints_py_3_9(values: list[typing.Union[str | int]]) -> str:
    return "OK: " + " + ".join(map(str, values))

print(handle_strings_or_ints_py_3_10([1, 2, "abc", 3.5]))

print(handle_strings_or_ints_py_3_9([1, 2, "abc", 3.5]))
