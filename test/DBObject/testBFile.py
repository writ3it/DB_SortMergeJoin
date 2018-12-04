import unittest
from DBObject.BufferedFile import BufferedFile
from DBObject.Buffer import Buffer
from DBObject.MemBlock import MemBlock

class FileTestCase(unittest.TestCase):

    def test_reading(self):
        size = 1000
        bSize = 10
        buffer = Buffer(noBlocks=10,blockSize=bSize)
        file = BufferedFile( buffer, size=size,valueSize=5 )
        expected = 1000 / 10
        i = 0
        while not file.eof():
            block = file.read()
            self.assertIsInstance(block, MemBlock)
            self.assertEqual(i*bSize, block.GetPosition(),msg="Niewłaściwa lokalizacja bloków")
            i = i + 1
        self.assertEqual(expected, i, msg="Odczytano niewłasciwą liczbę bloków")

if __name__ == '__main__':
    unittest.main()