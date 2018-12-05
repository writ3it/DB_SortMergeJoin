
import math

class MemBlock:

    def __init__(self, firstIndex, valueSize, size):
        self._firstIndex = firstIndex
        self._valueSize = valueSize
        self._size = size
        self._line = 0

    def eob(self):
        return self._line >= self._size

    def size(self):
        return self._size

    def GetPosition(self):
        return self._firstIndex

    def GetOffset(self):
        return self._line

    def seek(self, offset:int):
        self._line = offset

    def readRow(self):
        value = math.floor( (self._firstIndex+self._line) / self._valueSize )
        self._line = self._line + 1
        ''' FROMAT
        R[A], row_id_r, block_begin_index_r, S[A], row_id_s, block_begin_index_s
        '''
        return [value,self._firstIndex+self._line,self.GetPosition()]
