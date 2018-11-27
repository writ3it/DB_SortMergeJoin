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
        diff = self._size - self._index
        bs = self._blockSize
        if (diff<bs):
            bs = diff
        block = MemBlock(firstIndex = self._index, valueSize = self._valueSize, size = bs)
        self._index = self._index + self._blockSize
        return block

    def seek(self, offset):
        '''
        It doesn't guarantee alignment to block size but, why should be? :)
        '''
        self._index = offset

    def index(self):
        return self._index
