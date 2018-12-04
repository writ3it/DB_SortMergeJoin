from .File import File
from .Buffer import Buffer

'''
Responsibility:
- this class checks that block is in buffer. If is, buffer is used, otherwise disk (File object)
'''
class BufferedFile(File):

    def __init__(self, buffer:Buffer, size:int, valueSize:int ):
        super(BufferedFile, self).__init__(buffer.GetBlockSize(), size,valueSize)
        self.buffer = buffer
        pass

    def read(self):
        _id = id(self)
        index = self._index
        if not self.buffer.ContainBlockFor(_id,index):
            data = super(BufferedFile, self).read()
            self.buffer.StoreBlock(_id,data)
        return self.buffer.ReadBlock(_id,index)







