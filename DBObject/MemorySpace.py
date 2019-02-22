from DBObject.DataFile import DataFile


class MemorySpace:

    def __init__(self, buffer, no_blocks):
        self.size = no_blocks
        self.file = None
        self.idx = -1
        self.bufferedBlocks = []
        self.lastBlockCursor = -1

    def SetDataFile(self, file: DataFile):
        self.file = file

    def NextRow(self):
        if self.Eof():
            raise Exception("File attached to MemorySpace overflow")
        self.idx += 1
        return self.Read()

    def Read(self):
        self.loadBlocksIfShouldBe()
        for block in self.bufferedBlocks:
            if block.GetStartIdx() <= self.idx <= block.GetEndIdx():
                return block.ReadRow(self.idx)
        raise Exception("Something went wrong idx="+str(self.idx)+" file="+self.file.GetName())

    def loadBlocksIfShouldBe(self)->None:
        while not self.Contains(self.idx) and not self.file.Eof():
            self._loadNextBlock()

    def _loadNextBlock(self)->None:
        block = self.file.NextBlock()
        self.lastBlockCursor = (self.lastBlockCursor + 1) % self.size
        if len(self.bufferedBlocks)<self.size:
            self.bufferedBlocks.append(block)
        else:
            self.bufferedBlocks[self.lastBlockCursor] = block

    def Contains(self, idx: int)->bool:
        for block in self.bufferedBlocks:
            if block.GetStartIdx() <= idx <= block.GetEndIdx():
                return True
        return False

    def Eof(self):
        return not self.file.Contains(self.idx+1) and not self.Contains(self.idx+1)

    def Reset(self):
        self.idx = -1
        self.file.Reset()

