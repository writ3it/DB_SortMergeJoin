import unittest
from DBObject.File import File
from DBObject.MemBlock import MemBlock

class FileTestCase(unittest.TestCase):

    def test_count(self):
        file = File(blockSize=10,size=1000,valueSize=5)
        self.assertEqual(1000, file.size())

    def test_file_read(self):
        size = 1000
        bSize = 10
        file = File(blockSize=bSize, size=size, valueSize=5)
        expected = 1000/10
        i = 0
        while not file.eof():
            i = i + 1
            block = file.read()
            self.assertIsInstance(block, MemBlock)
        self.assertEqual(expected,i,msg="Odczytano niewłasciwą liczbę bloków")


if __name__ == '__main__':
    unittest.main()