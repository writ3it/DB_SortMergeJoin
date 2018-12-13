from .MemBlock import MemBlock

class File:

    def __init__(self, blockSize, size, valueSize):
        if valueSize<0:
            raise Exception("invalid valueSize")
        if size<0:
            raise Exception("invalid valueSize")
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
        if diff <= 0:
            raise Exception("EOF")
        bs = self._blockSize
        if (diff<bs):
            bs = diff
        block = MemBlock(firstIndex = self._index, valueSize = self._valueSize, size = bs)
        self._inc_index(self._index)
        return block

    def _inc_index(self, base):
        self._index = base + self._blockSize

    def seek(self, offset):
        '''
        It doesn't guarantee alignment to block size but, why should be? :)
        '''
        self._index = offset

    def index(self):
        return self._index
