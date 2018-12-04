from .BufferedFile import BufferedFile

class RowAccess:

    def __init__(self, file:BufferedFile):
        self.file = file
        self._state = False
        self.block = False
        self._lastRow = False

    def eof(self):
        return self.file.eof()

    def current(self,col=False):
        if col is False:
            return self._lastRow
        return self._lastRow[col]

    def readRow(self):
        if self.block is False:
            self.block = self.file.read()
        row = self.block.readRow()
        self._lastRow = row
        if self.block.eob():
            self.block = False
        return row


    def savePosition(self):
        if self.block is False:
            self.block = self.file.read()
        self._state = (
            self.block.GetPosition(),
            self.block.GetOffset()
        )

    def restorePosition(self):
        self.file.seek(self._state[0])
        self.block = self.file.read()
        self.block.seek(self._state[1])

