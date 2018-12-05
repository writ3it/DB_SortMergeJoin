from .File import File
from .Buffer import Buffer

'''
Responsibility:
- this class checks that block is in buffer. If is, buffer is used, otherwise disk (File object)
- counts access to disk
'''
class BufferedFile(File):

    def __init__(self, buffer:Buffer, size:int, valueSize:int ):
        super(BufferedFile, self).__init__(buffer.GetBlockSize(), size,valueSize)
        self.buffer = buffer
        self.counter = {
            self.COUNTER_DISK_READS: 0,
            self.COUNTER_BUFFER_READS: 0
        }

    COUNTER_DISK_READS = 'diskReads'
    COUNTER_BUFFER_READS = "bufferREADS"

    def read(self):
        _id = id(self)
        idx = self.index()
        exists = self.buffer.ContainBlockFor(_id,idx)
        if not exists:
            self.__inc_counter(self.COUNTER_DISK_READS)
            data = super(BufferedFile, self).read()
            self.buffer.StoreBlock(_id,data)
        else:
            self.__inc_counter(self.COUNTER_BUFFER_READS)
            self._inc_index(idx)
        return self.buffer.ReadBlock(_id,idx)

    def __inc_counter(self,name, step=1):
        val = self.counter[name]
        self.counter[name] = val + step

    def GetCounterVal(self, name:str):
        return self.counter[name]







