from .BufferedFile import BufferedFile

class RowAccess:

    def __init__(self, file:BufferedFile):
        self.file = file
        self._state = False
        self.block = False
        self._lastRow = False

    def eof(self):
        return self.file.eof() and ( self.block is not False and self.block.eob() or self.block is False)

    def current(self,col=False):
        if col is False:
            return self._lastRow
        return self._lastRow[col]

    def readRow(self):
        if self.block is False:
            self.block = self.file.read()
        try:
            row = self.block.readRow()
        except Exception:
            if self.file.eof():
                return False
            self.block = self.file.read()
            return self.readRow()
        self._lastRow = row
        return row


    def savePosition(self):
        if self.block is False :
            self.block = self.file.read()
        self._state = (
            self.block.GetPosition(),
            self.block.GetOffset()-1  # DANGER, effect of main loop (prefetching row in recursion)
        )

    def restorePosition(self):
        self.file.seek(self._state[0])
        self.block = self.file.read()
        self.block.seek(self._state[1])
        self._lastRow = self.block.readRow()


    def debugBlock(self):
        if (self.block == False):
            print("Block is False")
            return
        print("---")
        print(self.file.index())
        print(self.block.GetPosition())
        print(self.block.GetOffset())
        print("---")

