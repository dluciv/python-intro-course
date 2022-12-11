#!/usr/bin/env python3

def handle_simple(i: int) -> None:
    print(str(i) + "abc")

handle_simple('123')

def handle_strings_or_ints(values: list[str | int]) -> str:
    return " + ".join(map(str, values))

print(handle_strings_or_ints([1, 2, "abc", 3.5]))
