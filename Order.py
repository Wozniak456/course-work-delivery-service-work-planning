class Order:
    def __init__(self, i, t, d, w):
        self.i = i
        self.t = t
        self.d = d
        self.w = w
        self.T = t

    def print_order(self):
        print(f"The {self.i} order : t = {self.t} days, d = {self.d} days, w = {self.w} UAH. T[{self.i}] = {self.T}")