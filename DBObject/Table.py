
from DBObject.MemorySpace import MemorySpace


class Table:

    def __init__(self, file, buffer_space: MemorySpace):
        self.file = file
        self.buffer = buffer_space
        self.buffer.SetDataFile(file)
        #improve performance
        self.Reset = self.buffer.Reset
        self.GetSize = self.file.GetSize
        self.blockSize = self.file.BlockSize
        self.NextRow = self.buffer.NextRow
        self.Eof = self.buffer.Eof

    def GetRows(self):
        self.Reset()
        nextRow = self.NextRow
        n = self.GetSize()*self.blockSize()
        for _ in range(0, n):
            yield nextRow()