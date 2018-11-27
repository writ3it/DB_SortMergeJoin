import unittest
from DBObject.File import File

class FileTestCase(unittest.TestCase):

    def test_count(self):
        file = File(blockSize=10,size=1000,valueSize=5)
        self.assertEqual(1000, file.size())

if __name__ == '__main__':
    unittest.main()