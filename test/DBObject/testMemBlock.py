import unittest
from DBObject.File import File
from DBObject.MemBlock import MemBlock

class MemBlockTestCase(unittest.TestCase):

    def test_reading_data(self):
        size = 1000
        bSize = 10
        valueSize=5
        file = File(blockSize=bSize, size=size, valueSize=valueSize)
        value = 0
        i = 0
        while not file.eof():
            block = file.read()
            while not block.eob():
                line = block.readRow()
                # \/ uncomment this if you want to see results!
                # print(line,value)
                self.assertEqual(value, line['A'])
                i = i + 1
                if i % valueSize == 0:
                    value = value + 1

    def test_seek(self):
        size=100
        bSize=100
        valueSize=10
        file = File(blockSize=bSize,size=size,valueSize=valueSize)
        data = self._all_data_to_list(file)
        file.seek(0)
        data2 = self._all_data_to_list(file)
        self.assertEqual(True, data == data2)
        file.seek(17)
        data3 = self._all_data_to_list(file)
        self.assertEqual(size-17, len(data3))



    def _all_data_to_list(self,file):
        data = []
        while not file.eof():
            block = file.read()
            while not block.eob():
                line = block.readRow()
                data.append(line[0])
        return data

if __name__ == '__main__':
    unittest.main()