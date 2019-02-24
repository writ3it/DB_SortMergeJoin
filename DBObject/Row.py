
class Row:

    def __init__(self, data:list, row_id:int):
        self.__data = data
        self.row_id = row_id
        self.Get = self.__getitem__

    def GetId(self):
        return self.row_id

    def __getitem__(self, item):
        return self.__data[item]

    def __setitem__(self, key, value):
        raise Exception('Cannot modify data!')

    def __delitem__(self, key):
        raise Exception('Cannot modify data!')

    def Merge(self, row)->list:
        return self.__data + row.__data

