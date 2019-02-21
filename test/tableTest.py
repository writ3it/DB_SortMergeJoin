import unittest

from DBObject.Buffer import Buffer
from DBObject.DataFile import DataFile
from DBObject.Table import Table
class NestedLoopTest(unittest.TestCase):


    def test_iterate_over_all(self):
        no_blocks = 100
        block_size = 5
        key_size = 1
        buffer = Buffer(M=100)
        fR = DataFile(file_size_in_blocks=no_blocks, key_size=key_size, block_size=block_size)
        R = Table(fR, buffer.GetMemorySpace(1))

        i = 0

        while not R.Eof():
            row = R.NextRow()
            self.assertEqual(i, row[0],msg="Step Error")
            i += key_size
            self.assertGreaterEqual(no_blocks*block_size, i, msg="Limit")
        self.assertEqual(no_blocks * block_size, i, "Total outside")

    def test_neasted_iterations(self):
        no_blocks = 100
        block_size = 5
        key_size = 1
        buffer = Buffer(M=100)
        fR = DataFile(file_size_in_blocks=no_blocks, key_size=key_size, block_size=block_size)
        fS = DataFile(file_size_in_blocks=no_blocks, key_size=key_size, block_size=block_size)
        R = Table(fR, buffer.GetMemorySpace(1))
        S = Table(fS, buffer.GetMemorySpace(1))

        i = 0

        while not R.Eof():
            row = R.NextRow()
            j = 0
            while not S.Eof():
                nrow = S.NextRow()
                self.assertEqual(j, nrow[0], msg="Nested step Error")
                j += key_size
                self.assertGreaterEqual(no_blocks * block_size, j, msg="Nested limit")
            S.Reset()
            self.assertEqual(i, row[0], msg="Step Error")
            i += key_size
            self.assertGreaterEqual(no_blocks * block_size, i, msg="Limit")

        self.assertEqual(no_blocks * block_size, i, "Total outside")
        self.assertEqual(no_blocks * block_size, j, "Total inside")
