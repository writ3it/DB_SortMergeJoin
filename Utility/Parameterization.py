import math

class Parametrization:

    def __init__(self):
        self.__r_size = 0
        self.__s_size = 0
        self.__r_key_size = 0
        self.__s_key_size = 0
        self.__good_data = 0
        self.__waste_data = 0
        self.__selectivity = 0
        self.__buffer_size = 0
        self.__block_size = 0
        self.__total_size = 0
        self.__size = 0
        self.__r_buffer_size = 0
        self.__s_buffer_size = 0

    def SetSize(self, blocks:int):
        self.__size = blocks
        return self

    # Selectivity = no_rows after join  / no_rows(R) * no_rows(S)
    # Selectivity in %
    def SetSelectivity(self, s: float):
        if s < 0 or s > 1:
            raise Exception("Invalid value of selectivity")
        self.__selectivity = s
        return self

    # M - number of blocks
    # n - block size
    def SetBufferSize(self, M: int, n: int):
        self.__buffer_size = M
        self.__block_size = n
        return self

    def recalculate(self):
        s = self.__selectivity
        self.__r_key_size = 1
        self.__s_key_size = 1
        self.__r_size = self.__size * self.__block_size
        self.__s_size = self.__r_size
        self.__total_size = self.__r_size
        self.__good_data = math.ceil(math.sqrt(s*(self.__total_size**2)))
        self.__waste_data = self.__total_size - self.__good_data

    def RealSelectivity(self):
        return (self.__good_data**2) / (self.__total_size ** 2)

    def GetRSize(self)->int:
        return self.__r_size

    def GetSSize(self)->int:
        return self.__s_size

    def GetRKeySize(self):
        return self.__r_key_size

    def GetSKeySize(self):
        return self.__s_key_size

    def GetGoodDataSize(self):
        return self.__good_data

    def GetWasteDataSize(self):
        return self.__waste_data

    def GetBufferSize(self):
        return self.__buffer_size

    def GetBlockSize(self):
        return self.__block_size

    def GetTotalSize(self):
        return self.__total_size

    def GetRBufferSize(self):
        return self.__r_buffer_size

    def GetSBufferSize(self):
        return self.__s_buffer_size

    def SetRBufferSize(self, n: int):
        self.__r_buffer_size = n
        return self

    def SetSBufferSize(self, n: int):
        self.__s_buffer_size = n
        return self


