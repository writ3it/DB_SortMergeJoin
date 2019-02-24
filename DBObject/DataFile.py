from DBObject.DataBlock import DataBlock


class DataFile:

    def __init__(self, file_size_in_blocks: int, key_size: int, block_size: int, name: str="File"):
        self.fileSize = file_size_in_blocks
        self.keySize = key_size
        self.blockSize = block_size
        self.blockReadedIdx = 0
        self.readedIdx = 0
        self.name = name

    def Reset(self)->None:
        self.readedIdx = 0
        self.blockReadedIdx = 0

    def Seek(self, idx: int)->None:
        self.blockReadedIdx = self.calcBlockIdx(idx)+1
        self.readedIdx = self.blockReadedIdx * self.blockSize

    def LoadBlockWith(self, idx: int)->DataBlock:
        if not self.Contains(idx):
            raise Exception("Idx doesn't exists")
        bIdx = self.calcBlockIdx(idx)
        rIdx = bIdx * self.blockSize
        return DataBlock(rIdx, self.keySize, self.blockSize)

    def Eof(self)->bool:
        return self.blockReadedIdx == self.fileSize

    def Contains(self, idx):
        return 0 <= idx <= self.blockSize*self.fileSize -1

    def BlockSize(self):
        return self.blockSize

    def GetSize(self):
        return self.fileSize

    def GetName(self):
        return self.name

    def NextBlock(self)->DataBlock:
        if self.Eof():
            raise Exception("File overflow")
        block = DataBlock(self.readedIdx, self.keySize, self.blockSize)
        self.readedIdx += self.blockSize
        self.blockReadedIdx += 1
        return block

    def GetLastRowId(self)->int:
        return self.readedIdx - 1

    def calcBlockIdx(self, idx):
        return idx // self.blockSize




