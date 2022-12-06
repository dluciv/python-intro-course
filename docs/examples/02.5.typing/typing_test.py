#!/usr/bin/env -S python3.11

from numbers import Number
from typeguard import typechecked

@typechecked
def handle_simple(i: Number) -> None:
    print(str(i) + "abc")

handle_simple(123)

@typechecked
def handle_strings_or_ints(values: list[str | int]) -> str:
    return " + ".join(map(str, values))

print(handle_strings_or_ints([1, 2, "abc", 3.5]))
