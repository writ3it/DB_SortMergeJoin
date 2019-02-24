
class JoinMeta:

    def JoinMeta(self):
        self._outputSize = 0

    def join(self, leftRelation, rightRelation, condition):
        self._outputSize = 0

    def mergeOutputRow(self, row_l, row_r):
        #print(row_l.Merge(row_r))
        self._outputSize += 1
        pass

    def GetOutputSize(self):
        return self._outputSize


EQUAL = lambda a, b: a[0] == b[0]
