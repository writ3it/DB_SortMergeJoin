
import math

class MemBlock:

    def __init__(self, firstIndex, valueSize, size):
        self._firstIndex = firstIndex
        self._valueSize = valueSize
        self._size = size
        self._line = 0

    def eob(self):
        return self._line >= self._size

    def readRow(self):
        value = math.floor( (self._firstIndex+self._line) / self._valueSize )
        self._line = self._line + 1
        return [value]
