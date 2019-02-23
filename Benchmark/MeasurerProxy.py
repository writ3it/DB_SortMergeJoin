
from Benchmark.Counter import Counter


class MeasurerProxy:
    def __init__(self, obj, counter: Counter, name:str = "Measure"):
        self.object = obj
        self.observed_calls = counter.GetObserved()
        self.counter = counter

    def __getattr__(self, name):
        if name in self.observed_calls:
            self.counter.Hit()

        def method(*args):
            return getattr(self.object, name)(*args)
        return method
