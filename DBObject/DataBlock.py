
class DataBlock:

    def __init__(self, start_idx: int, key_size: int, no_rows: int):
        self.start_idx = start_idx
        self.key_size = key_size
        self.no_rows = no_rows

    def GetStartIdx(self)->int:
        return self.start_idx

    def GetEndIdx(self)->int:
        return self.start_idx + self.no_rows - 1

    def GetRows(self):
        readRow = self.ReadRow
        return map(lambda i: readRow(i), range(self.GetStartIdx(),self.GetEndIdx()+1))

    def ReadRow(self, idx: int):
        keyValue = self.calcKeyAttributevalue(idx)
        return [keyValue]

    def calcKeyAttributevalue(self, row_id: int)->int:
        return row_id // self.key_size

    def Contains(self, idx):
        return self.GetStartIdx() <= idx <= self.GetEndIdx()
