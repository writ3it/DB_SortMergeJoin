
class JoinMeta:
    def join(self, leftRelation, rightRelation, condition):
        pass

    def mergeOutputRow(self, row_l, row_r):
        print((row_l, row_r),flush=True)
        pass


EQUAL = lambda a, b: a[0] == b[0]
