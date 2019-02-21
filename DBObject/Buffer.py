from .MemorySpace import MemorySpace

class Buffer:

    def __init__(self, M):
        self.bufferSize = M
        self.notUsedBlocks = M
        self.counter = 0


    def GetMemorySpace(self, noBlocks):
        if noBlocks>self.notUsedBlocks:
            raise Exception("Not enought memory!")
        return MemorySpace(self, noBlocks)

    def GetDiskHitsCounter(self):
        return self.counter