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
                self.assertEqual(value, line[0])
                i = i + 1
                if i % valueSize == 0:
                    value = value + 1

if __name__ == '__main__':
    unittest.main()