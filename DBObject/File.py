
class File:

    def __init__(self, blockSize, size, valueSize):
        self.blockSize = blockSize
        self.size = size
        self.valueSize = valueSize
        self.index = 0

    def eof(self):
        return self.index >= size

    def size(self):
        return self.size