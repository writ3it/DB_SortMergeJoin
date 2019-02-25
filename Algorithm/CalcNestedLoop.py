
from Operator import Join
from DBObject.Table import Table
from typing import Callable, List
from Benchmark.Counter import Counter


class CalcNestedLoop(Join.JoinMeta):

    def __init__(self):
        super().__init__()
        self._counter = None

    def SetCounter(self,counter:Counter):
        self._counter = counter

    # join method
    # Block Nested Loop, better than naive
    def join(self, left_relation: Table, right_relation: Table, condition: Callable[[List[int], List[int]], bool]):
        v = left_relation.GetSize() * right_relation.GetSize() + left_relation.GetSize()
        self._counter.SetValue(v)



