#!/usr/bin/env python3

import module1
import module2

from module1 import *
from module2 import *

print(m1f1())

# print(_m1f2()) вызовет ошибку, так как с _ начинаются внутренние имена
print(module1._m1f2())  # а так можно

print(m2f1())
# print(m2f2()) вызовет ошибку, так как с m2f2 явно не указано в __all__ в module2
print(module2.m2f2())  # а так можно
