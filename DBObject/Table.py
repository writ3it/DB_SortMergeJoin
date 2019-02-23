from DBObject.MemorySpace import MemorySpace
import math


class Table:

    def __init__(self, file, buffer_space: MemorySpace):

        self.file = file
        self.buffer = buffer_space
        self.buffer.SetDataFile(file)
        self.GetPart = self.buffer.GetPart
        #improve performance
        self.Reset = self.buffer.Reset
        self.GetSize = self.file.GetSize
        self.blockSize = self.file.BlockSize
        self.NextRow = self.buffer.NextRow
        self.NextBlock = self.buffer.GetPart
        self.Eof = self.buffer.Eof

    def GetBufferedBlocks(self):
        self.Reset()
        nextPart = self.GetPart
        n = math.ceil(self.GetSize() / self.buffer.GetSize())
        for i in range(0, n):
            yield list(nextPart())

    def GetRows(self):
        self.Reset()
        nextRow = self.NextRow
        n = self.GetSize()*self.blockSize()
        for i in range(0, n):
            yield nextRow()
