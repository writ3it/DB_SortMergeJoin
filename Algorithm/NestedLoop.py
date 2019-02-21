
from Operator import Join
from DBObject.Table import Table
from typing import Callable, List


class NestedLoop(Join.JoinMeta):

    # join method
    # Naive Nested Loop
    def join(self, left_relation: Table, right_relation: Table, condition: Callable[[List[int], List[int]], bool]):
        for row_l in left_relation.GetRows():
            for row_r in right_relation.GetRows():
                if condition(row_l, row_r):
                    self.mergeOutputRow(row_l, row_r)
