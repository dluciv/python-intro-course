import module1  # !!! очень подозрительно — import чего-то «сверху»

def p1m1f1():
    return 'p1m1f1 -> ' + module1.m1f1()
