
from DBObject.MemorySpace import MemorySpace


class Table:

    def __init__(self, file, buffer_space: MemorySpace):
        self.file = file
        self.buffer = buffer_space
        self.buffer.SetDataFile(file)

    def Eof(self):
        return self.buffer.Eof()

    def NextRow(self):
        return self.buffer.NextRow()

    def GetRows(self):
        self.Reset()
        while not self.Eof():
            yield self.NextRow()

    def Reset(self):
        self.buffer.Reset()