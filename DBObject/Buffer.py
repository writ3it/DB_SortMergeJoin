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
        self.bufferSize = noBlocks
        self.currentSize = 0
        self.index = []
        self.counter = {}
        self.blockSize = blockSize
        self.time = 0
        pass

    def _tick(self):
        self.time = self.time + 1

    def Time(self):
        return self.time

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

        self.currentSize = self.currentSize - 1
        times = [row['time'] for row in self.index]
        minTime = min(times)
        idxItems = [{'fileName':row['fileName'],'pos':row['pos'],'index':(row['index']-1) ,'time':row['time'],'data':row['data']} for row in self.index if row['time'] == minTime]
        self.index = [{'fileName':row['fileName'],'pos':row['pos'],'index':(row['index']-1),'time':row['time'],'data':row['data'] } for row in self.index if row['time'] > minTime]
        for idxItem in idxItems:
            self._inc_counter(idxItem, 0, 1)
        self._tick()


    def addNew(self, fileName:str, memBlock:MemBlock):
        idxItem = {'fileName': fileName, 'pos': memBlock.GetPosition(), 'index': self.currentSize, 'time':self.Time(),'data':memBlock}
        self.index.append(idxItem)
        self.currentSize = self.currentSize + 1
        self._inc_counter(idxItem,1,0)
        self._tick()

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

    def Debug(self):
        counts = {}
        for i in self.index:
            if not i['fileName'] in counts:
                counts[i['fileName']] = 0
            counts[i['fileName']] = counts[i['fileName']] + 1
        print(str(len(self.index))+" "+ " "+str(counts))

    def GetIndexesIn(self):
        return [row['pos'] for row in self.index]

    def ReadCounter(self,filename:str, pos:int, type:str):
        return self.counter[filename][pos][type];

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
        for i,f in enumerate(self.index):
            if f['index'] is index['index']:
                self.index[i]['time'] = self.Time()

        self._tick()
        return index['data']
