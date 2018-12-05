from .MemBlock import MemBlock
from collections import deque
'''
Responsibility:
- stores blocks of data

index - row index
'''
class Buffer:

    '''
    Constructor
    noBlocks - number of Blocks to manage in Buffer
    '''
    def __init__(self, noBlocks:int, blockSize:int):
        self.blocks = deque([])
        self.bufferSize = noBlocks
        self.currentSize = 0
        self.index = []
        self.counter = {}
        self.blockSize = blockSize
        pass

    def GetSize(self):
        return self.currentSize

    def IsFull(self):
        return self.currentSize >= self.bufferSize

    def GetBlockSize(self):
        return self.blockSize


    def StoreBlock(self,fileName:str, memBlock:MemBlock):
        self.removeOlds()
        self.addNew( fileName, memBlock)


    def removeOlds(self):
        while self.IsFull():
            self._removeOld()

    def _removeOld(self):
        removed = self.blocks.popleft()
        self.currentSize = self.currentSize - 1
        self.index = [{'fileName':row['fileName'],'pos':row['pos'],'index':(row['index']-1) } for row in self.index if row['index'] > 0]


    def addNew(self, fileName:str, memBlock:MemBlock):
        self.blocks.append(memBlock)
        idxItem = {'fileName': fileName, 'pos': memBlock.GetPosition(), 'index': self.currentSize}
        self.index.append(idxItem)
        self.currentSize = self.currentSize + 1
        self._inc_counter(idxItem,1,0)

    def _inc_counter(self,item,add,remove):
        if item['fileName'] not in self.counter:
            self.counter[item['fileName']] = {}

        if item['pos'] not in self.counter[item['fileName']]:
            self.counter[item['fileName']][item['pos']] = {'add':0,'remove':0}

        current = self.counter[item['fileName']][item['pos']]
        self.counter[item['fileName']][item['pos']] = {
            'add': current['add']+add,
            'remove': current['remove']+remove
        }

    def PrintCounter(self):
        print(self.counter)

    def FindIndexToRead(self,fileName:str, index:int):
        return [row for row in self.index if (row['fileName'] == fileName and row['pos'] == index)]

    def ContainBlockFor(self,fileName:str, index:int)->bool:
        res =  len(self.FindIndexToRead(fileName,index))>0
        return res

    def ReadBlock(self, fileName:str, index:int)->MemBlock:
        el = self.FindIndexToRead(fileName, index)
        index = el.pop()
        block = self.blocks[index['index']] # too many indexes :D
        return block
