from .MemBlock import MemBlock

class File:

    def __init__(self, blockSize, size, valueSize):
        self._blockSize = blockSize
        self._size = size
        self._valueSize = valueSize
        self._index = 0

    def eof(self):
        return self._index >= self._size

    def size(self):
        return self._size

    def read(self):
        block = MemBlock(firstIndex = self._index, valueSize = self._valueSize, size = self._blockSize)
        self._index = self._index + self._blockSize
        return block
