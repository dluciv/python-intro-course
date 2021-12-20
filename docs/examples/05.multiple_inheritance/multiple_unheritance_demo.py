class SimpleA:
    def __init__(self, p):
        print(f'SimpleA constructor for object of {type(self)} with param {p}')

class SimpleB(SimpleA):
    def __init__(self, p):
        super().__init__(p)
        print(f'SimpleB constructor for object of {type(self)} with param {p}')

class SimpleC(SimpleA):
    def __init__(self, p):
        super().__init__(p + 1)
        print(f'SimpleC constructor for object of {type(self)} with param {p}')

class SimpleD(SimpleB, SimpleC):
    def __init__(self):
        super().__init__(1)
        print(f'SimpleD constructor for object of {type(self)}')

print("Simple case:")
sd = SimpleD()
print("============")

class ComplicatedC1(SimpleA):
    def __init__(self, vc1, vc2):
        super().__init__()
        print(f'ComplicatedC1 constructor for object of {type(self)} with params {vc1}, {vc2}')

class ComplicatedC2(SimpleA):
    def __init__(self, vc1, vc2):
        super().__init__()
        print(f'ComplicatedC2 constructor for object of {type(self)} with params {vc1}, {vc2}')

class ComplicatedD(SimpleB, ComplicatedC1, ComplicatedC2):
    def __init__(self):
        try:
            SimpleB.__init__(self, -1)
        except TypeError as te:
            print(f"Eah, everything goes as [un]expected: {te}")
            print("See https://stackoverflow.com/a/34885285/539470")
        # super(ComplicatedC1, self).__init__('[vc1]', '[vc2]')
        # super(ComplicatedC2, self).__init__('[vc1]', '[vc2]')
        print(f'ComplicatedD constructor for object of {type(self)}')

print("Complicated case:")
cd = ComplicatedD()
print("============")
