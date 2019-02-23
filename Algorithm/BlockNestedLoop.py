
from Operator import Join
from DBObject.Table import Table
from typing import Callable, List


class BlockNestedLoop(Join.JoinMeta):

    # join method
    # Block Nested Loop, better than naive
    def join(self, left_relation: Table, right_relation: Table, condition: Callable[[List[int], List[int]], bool]):
        mergeFunction = self.mergeOutputRow
        rightBlocks = right_relation.GetBufferedBlocks
        leftRows = left_relation.GetRows
        for loadedBlocks in right_relation.GetBufferedBlocks():
            for row_l in left_relation.GetRows():
                for block_r in loadedBlocks:
                    for row_r in block_r.GetRows():
                        if condition(row_l, row_r):
                            mergeFunction(row_l, row_r)

