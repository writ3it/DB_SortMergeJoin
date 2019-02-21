from DBObject.DataBlock import DataBlock


class DataFile:

    def __init__(self, file_size_in_blocks:int, key_size:int, block_size:int):
        self.fileSize = file_size_in_blocks
        self.keySize = key_size
        self.blockSize = block_size
        self.blockReadedIdx = 0
        self.readedIdx = 0

    def Reset(self)->None:
        self.readedIdx = 0
        self.blockReadedIdx = 0


    def Eof(self)->bool:
        return self.blockReadedIdx == self.fileSize

    def NextBlock(self)->DataBlock:
        if self.Eof():
            raise Exception("File overflow")
        block = DataBlock(self.readedIdx, self.keySize, self.blockSize)
        self.readedIdx += self.blockSize
        self.blockReadedIdx += 1
        return block




