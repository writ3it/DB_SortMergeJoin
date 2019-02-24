from DBObject.DataFile import DataFile
from DBObject.DataBlock import DataBlock
from functools import reduce


class MemorySpace:

    def __init__(self, buffer, no_blocks):
        self.size = no_blocks
        self.file = None
        self.idx = -1
        self.bufferedBlocks = []
        self.lastBlockCursor = -1
        self.partSize = 0
        #cannot rewrite file.NextBlock because it's observed by proxy!
        #when you assign to field it will not be observed
        self.__light_contains = False
        self._fileContains = None
        self._fileEof = None
        self._fileReset = None
        self._readedBlocks = 0

    def GetLastRowId(self):
        return self.idx

    def RewindTo(self, idx:int)->None:
        if not self.file.Contains(idx):
            raise Exception("Idx doesn't exists")
        if not self.Contains(idx):
            block = self.file.LoadBlockWith(idx)
            self.bufferBlock(block)
        else:
            block = self.getBlockContains(idx)
        self._readedBlocks = block.GetBlockId()+1
        self.idx = idx
        self.file.Seek(idx)
        return block.ReadRow(idx)

    def GetSize(self)->int:
        return self.size

    def GetPart(self):
        n = self.size
        if self._readedBlocks+n > self.file.GetSize():
            n = self.file.GetSize() - self._readedBlocks
        self._readedBlocks += n
        self.idx += self.partSize
        file = self.file
        return map(lambda i: file.NextBlock(), range(0, n))

    def SetDataFile(self, file: DataFile):
        self.file = file
        self._fileContains = self.file.Contains
        self._fileEof = self.file.Eof
        self._fileReset = self.file.Reset
        self.partSize = self.size * self.file.GetSize()

    def NextRow(self):
        if self.Eof():
            raise Exception("File attached to MemorySpace overflow")
        self.idx += 1
        return self.Read()


    def Read(self):
        self.loadBlocksIfShouldBe()
        return self.getBlockContains(self.idx).ReadRow(self.idx)

    def getBlockContains(self, idx) -> DataBlock:
        for block in self.bufferedBlocks:
            if block.Contains(idx):
                return block
        raise Exception("Something went wrong idx="+str(self.idx)+" file="+self.file.GetName())


    def loadBlocksIfShouldBe(self)->None:
        self.__light_contains = self.Contains(self.idx)
        while not self.__light_contains and not self._fileEof():
            self._loadNextBlock()
            self.__light_contains = self.bufferedBlocks[self.lastBlockCursor].Contains(self.idx)

    def _loadNextBlock(self)->None:
        block = self.file.NextBlock()
        self._readedBlocks += 1
        self.bufferBlock(block)

    def bufferBlock(self, block:DataBlock)->None:
        self.lastBlockCursor = (self.lastBlockCursor + 1) % self.size
        if len(self.bufferedBlocks) < self.size:
            self.bufferedBlocks.append(block)
        else:
            self.bufferedBlocks[self.lastBlockCursor] = block

    def Contains(self, idx: int)->bool:
        if len(self.bufferedBlocks) == 0:
            return False
        states = map(lambda block: block.Contains(idx), self.bufferedBlocks)
        return reduce(lambda x, y: x or y, states)

    def Eof(self):
        return not self._fileContains(self.idx+1) and not self.Contains(self.idx+1)

    def Reset(self):
        self.idx = -1
        self._readedBlocks
        self._fileReset()

