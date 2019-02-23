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

    def test_iterate_over_all_by_block(self):
        no_blocks = 100
        block_size = 5
        key_size = 1
        buffer = Buffer(M=100)
        fR = DataFile(file_size_in_blocks=no_blocks, key_size=key_size, block_size=block_size)
        R = Table(fR, buffer.GetMemorySpace(5))

        i = 0
        for blocks in R.GetBufferedBlocks():
            for block in blocks:
                for row in block.GetRows():
                    self.assertEqual(i, row[0],msg="Step Error")
                    i += key_size
            self.assertGreaterEqual(no_blocks*block_size, i, msg="Limit")
        self.assertEqual(no_blocks * block_size, i, "Total outside")

    def test_nested_iterate_over_all_by_block(self):
        no_blocks = 100
        block_size = 5
        key_size = 1
        buffer = Buffer(M=100)
        fR = DataFile(file_size_in_blocks=no_blocks, key_size=key_size, block_size=block_size)
        fS = DataFile(file_size_in_blocks=no_blocks, key_size=key_size, block_size=block_size)
        R = Table(fR, buffer.GetMemorySpace(5))
        S = Table(fS, buffer.GetMemorySpace(5))

        no_b = 0
        i = 0
        repeated_rows = 0
        for blocks in R.GetBufferedBlocks():
            no_b += 1
            j = 0
            for lrow in S.GetRows():
                repeated_rows += 1
                for block in blocks:
                    for row in block.GetRows():
                        self.assertEqual(i, row[0], msg="Step Error Inner")
                        self.assertEqual(j, lrow[j], msg="Step Error Inner J")
                        i += key_size
                self.assertEqual(j, lrow[0], msg="Step Error Outter")
                j+=key_size
        self.assertEqual(no_b, no_blocks / 5)
        self.assertEqual(repeated_rows, (no_blocks / 5)*5*no_blocks,"Repeated rows")
        self.assertGreaterEqual(no_blocks * block_size, i, msg="Limit")
        self.assertEqual(no_blocks * block_size, i, "Total outside")

    def test_iterate_over_all_big_buffer(self):
        no_blocks = 50
        block_size = 5
        key_size = 1
        buffer = Buffer(M=100)
        fR = DataFile(file_size_in_blocks=no_blocks, key_size=key_size, block_size=block_size)
        R = Table(fR, buffer.GetMemorySpace(1))

        i = 0

        while not R.Eof():
            row = R.NextRow()
            self.assertEqual(i, row[0], msg="Step Error")
            i += key_size
            self.assertGreaterEqual(no_blocks * block_size, i, msg="Limit")
        self.assertEqual(no_blocks * block_size, i, "Total outside")

    def test_nested_iterations_big_buffer(self):
        no_blocks = 10
        block_size = 5
        key_size = 1
        buffer = Buffer(M=200)
        fR = DataFile(file_size_in_blocks=no_blocks, key_size=key_size, block_size=block_size, name="fR")
        fS = DataFile(file_size_in_blocks=no_blocks, key_size=key_size, block_size=block_size, name="fS")
        R = Table(fR, buffer.GetMemorySpace(100))
        S = Table(fS, buffer.GetMemorySpace(100))

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

    def test_nested_iterations(self):
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


    def test_with_generators(self):
        no_blocks = 100
        block_size = 5
        key_size = 1
        buffer = Buffer(M=100)
        fR = DataFile(file_size_in_blocks=no_blocks, key_size=key_size, block_size=block_size)
        fS = DataFile(file_size_in_blocks=no_blocks, key_size=key_size, block_size=block_size)
        R = Table(fR, buffer.GetMemorySpace(1))
        S = Table(fS, buffer.GetMemorySpace(1))

        i = 0
        for row in R.GetRows():
            j = 0
            for nrow in S.GetRows():
                self.assertEqual(j, nrow[0], msg="Nested step Error")
                j += key_size
                self.assertGreaterEqual(no_blocks * block_size, j, msg="Nested limit")
            S.Reset()
            self.assertEqual(i, row[0], msg="Step Error")
            i += key_size
            self.assertGreaterEqual(no_blocks * block_size, i, msg="Limit")

        self.assertEqual(no_blocks * block_size, i, "Total outside")
        self.assertEqual(no_blocks * block_size, j, "Total inside")
