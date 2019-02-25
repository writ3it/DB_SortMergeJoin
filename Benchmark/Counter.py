class Counter:
    def __init__(self):
        self.observed = []
        self.counter = 0

    def Observe(self, name: str)->None:
        self.observed.append(name)

    def GetObserved(self):
        return self.observed

    def Reset(self):
        self.counter = 0

    def Hit(self):
        self.counter += 1

    def GetValue(self):
        return self.counter

    def SetValue(self, n: int):
        self.counter = n