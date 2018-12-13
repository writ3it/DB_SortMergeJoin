import unittest
from DBObject.Buffer import  Buffer
from DBObject.MemBlock import MemBlock

class BufferTestCase(unittest.TestCase):

    def test_get_size(self):
        buffer = Buffer(10,10)
        self.assertEqual(0,buffer.GetSize())
        self.assertEqual(10,buffer.GetBlockSize())

    def test_add_remove(self):
        buffer = Buffer(10,10)
        self.assertEqual(0, buffer.GetSize())

        for i in range(10):
            memBlock = MemBlock(i*10, 1, 10)
            buffer.StoreBlock('test',memBlock)
            self.assertEqual(i+1, buffer.GetSize())
        good = []
        for i in range(10):
            good.append(i*10)
            memBlock = MemBlock(i * 10, 1, 10)
            buffer.StoreBlock('test',memBlock)
            self.assertEqual(10, buffer.GetSize())
            self.assertEqual(True, buffer.IsFull())

        self.assertEqual(good, buffer.GetIndexesIn())

        for i in range(10):
            buffer._removeOld()

        self.assertEqual(0, len(buffer.GetIndexesIn()))

        self.assertEqual(0, buffer.GetSize())


    def test_counter(self):
        buffer = Buffer(10, 10)
        memBlock = MemBlock(0, 1, 10)
        for i in range(20):
            buffer.StoreBlock('test',memBlock)

        self.assertEqual(20, buffer.ReadCounter('test', 0,'add'))
        self.assertEqual(10, buffer.ReadCounter('test', 0, 'remove'))




if __name__ == '__main__':
    unittest.main()