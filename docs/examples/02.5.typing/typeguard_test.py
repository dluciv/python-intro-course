#!/usr/bin/env python3

from numbers import Number
from typeguard import typechecked

@typechecked
def handle_simple(i: Number) -> None:
    print(str(i) + "abc")

handle_simple('123')
