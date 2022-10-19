class a:
    def __init__(self):
        self.var = 0

class b(a):
    def __init__(self):
        super().__init__()
        self.var2 = 0

    def __init__(self, var2):
        super().__init__()
        self.var2 = var2

    def abc(self):
        print("hellow")


