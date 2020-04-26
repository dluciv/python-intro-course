#!/usr/bin/env python3
from __future__ import annotations
from typing import List, Sequence
from typeguard import typechecked

import pint

import csv

u: pint.UnitRegistry = pint.UnitRegistry()

class Surface:
    def __init__(self, csv_filename: str):
        with open(csv_filename) as cfn:
            self._heights = [h for [h] in csv.reader(csv_filename)]

    def get_width(self):
        return 1500 * u.m

    def get_height(self, x):
        return x ** 2

s = Surface()
print(s.get_height(500 * (u.m ** 2)))

if __name__ == '__main__':
    raise NotImplementedError("This file is not supposed to be launched as a program")
