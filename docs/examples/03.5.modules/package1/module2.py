from . import module1  # а вот тут хорошо — import из своего пакета
from .subpack2 import module3 # или из пакета/модуля на одном уровне с собой

def p1m2f1():
    return 'p1m2f1 -> ' + module3.p1s2m3f1() + ' -> ' + module1.p1m1f1()
