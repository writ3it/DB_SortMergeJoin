from .MemBlock import MemBlock
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
    def __init__(self, noBlocks:int):
        pass


   def StoreBlock(self,fileName:str, memBlock:MemBlock):
       pass

   def ContainBlockFor(self,fileName:str, index:int)->bool:
       pass

   def ReadBlock(self,fileName:str, index:int)->MemBlock:
       pass