
import math

class MemBlock:

    def __init__(self, firstIndex, valueSize, size):
        self._firstIndex = firstIndex
        self._valueSize = valueSize
        self._size = size
        self._line = 0

    def eob(self):
        return self._line >= self._size

    def GetPosition(self):
        return self._firstIndex

    def GetOffset(self):
        return self._line

    def seek(self, offset:int):
        self._line = offset

    def readRow(self):
        value = math.floor( (self._firstIndex+self._line) / self._valueSize )
        self._line = self._line + 1
        return [value,self._firstIndex+self._line]
