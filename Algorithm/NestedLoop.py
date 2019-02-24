
from Operator import Join
from DBObject.Table import Table
from typing import Callable, List


class NestedLoop(Join.JoinMeta):

    # join method
    # Naive Nested Loop
    def join(self, left_relation: Table, right_relation: Table, condition: Callable[[List[int], List[int]], bool]):
        super().join(left_relation,right_relation,condition)
        mergeFunction = self.mergeOutputRow
        leftRows = left_relation.GetRows
        rightRows = right_relation.GetRows
        for row_l in leftRows():
            for row_r in rightRows():
                if condition(row_l, row_r):
                    mergeFunction(row_l, row_r)
