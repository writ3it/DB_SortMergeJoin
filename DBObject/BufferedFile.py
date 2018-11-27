from .File import File
from .Buffer import Buffer

'''
Responsibility:
- this class checks that block is in buffer. If is, buffer is used, otherwise disk (File object)
'''
class BufferedFile(File):

    def __init__(self), buffer:Buffer, blockSize:int, size:int, valueSize:int):
        pass


