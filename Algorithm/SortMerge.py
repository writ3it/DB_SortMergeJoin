from Operator import Join
from DBObject.Table import Table
from typing import Callable, List
import math

class SortMerge(Join.JoinMeta):



    # join method
    # Naive Nested Loop

    def join(self, left_relation: Table, right_relation: Table, condition: Callable[[List[int], List[int]], bool]):
        if condition != Join.EQUAL: # !!! presumption !!!
            raise Exception("condition should be Join.EQUAL - presumption")
        mergeFunction = self.mergeOutputRow
        leftRows = left_relation.GetRows
        rightRows = right_relation.GetRows

        # Step 1 - sort records ( presumption )

        left_relation.Reset()
        right_relation.Reset()

        A = 0


        join_finished = left_relation.Eof() or right_relation.Eof()

        cr_left = left_relation.NextRow()
        cr_right = right_relation.NextRow()
        left_a = cr_left[A]
        right_a = cr_right[A]

        while not join_finished:
            # find min Y

            while not condition(cr_left, cr_right):
                if left_a < right_a:
                    while cr_left[A] == left_a and not left_relation.Eof():
                        cr_left = left_relation.NextRow()
                    join_finished = left_relation.Eof()
                    left_a = cr_left[A]
                else:  # left_a >= right_a:
                    while cr_right[A] == right_a and not right_relation.Eof():
                        cr_right = right_relation.NextRow()
                    join_finished = right_relation.Eof()
                    right_a = cr_right[A]

            # mergeData - common buffer?
            right_rowid = right_relation.GetLastRowId()
            first_row = cr_right
            left_cond = True
            right_cond = True
            while left_cond and not left_relation.Eof(): # left relation
                while right_cond and not right_relation.Eof(): # right relation
                    self.mergeOutputRow(cr_left, cr_right)
                    cr_right = right_relation.NextRow()
                    right_cond = condition(cr_left, cr_right)
                cr_left = left_relation.NextRow()
                if condition(cr_left, first_row):
                    right_relation.RewindTo(row_id)
                else:
                    left_cond = right_cond = condition(cr_left, cr_right)
                    first_row = cr_right
                    right_rowid = right_relation.GetLastRowId()

            break

            # now condition is true






