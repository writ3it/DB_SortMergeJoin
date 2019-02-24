import unittest

from DBObject.Buffer import Buffer
from DBObject.DataFile import DataFile
from DBObject.Table import Table
from Algorithm.NestedLoop import NestedLoop
from Algorithm.BlockNestedLoop import BlockNestedLoop
from Algorithm.SortMerge import SortMerge
from Operator import Join


class KeySizeTest(unittest.TestCase):


    def test_iterate_over_all(self):
        no_blocks = 100
        block_size = 5
        key_size = 3
        buffer = Buffer(M=100)
        fR = DataFile(file_size_in_blocks=no_blocks, key_size=key_size, block_size=block_size)
        R = Table(fR, buffer.GetMemorySpace(1))

        i = 0

        for row in R.GetRows():
            v = i // key_size
            self.assertEqual(v, row[0], msg="Step Error i="+str(i))
            i += 1
        self.assertEqual(no_blocks * block_size, i, "Total outside")

    def _exp(self, algorithm, key_size_left, key_size_right):
        B_R = 50 * key_size_left
        B_S = 50 * key_size_right
        M = 10
        expected = 50 * 5 * key_size_left * key_size_right

        buffer = Buffer(M)
        fR = DataFile(B_R, key_size=key_size_left, block_size=5, name="fR")
        fS = DataFile(B_S, key_size=key_size_right, block_size=5, name="fS")

        R = Table(fR, buffer.GetMemorySpace(1))
        S = Table(fS, buffer.GetMemorySpace(9))

        self.assertEqual(B_R, R.GetSize(), "Size of R")
        self.assertEqual(B_S, S.GetSize(), "Size of S")

        algorithm.join(R, S, Join.EQUAL)

        self.assertEqual(expected, algorithm.GetOutputSize(), "Join R->S")

    def test_nested_loop(self):
        self._exp(NestedLoop(), 1, 3)
        self._exp(NestedLoop(), 2, 3)

    def test_nested_loop_rev(self):
        self._exp(NestedLoop(), 3, 1)
        self._exp(NestedLoop(), 3, 2)

    def test_block_nested_loop(self):
        self._exp(BlockNestedLoop(), 1, 3)
        self._exp(BlockNestedLoop(), 2, 3)

    def test_block_nested_loop_rev(self):
        self._exp(BlockNestedLoop(), 3, 1)
        self._exp(BlockNestedLoop(), 3, 2)

    def test_sort_merge(self):
        self._exp(SortMerge(), 1, 3)
        self._exp(SortMerge(), 2, 3)

    def test_sort_merge_rev(self):
        self._exp(SortMerge(), 3, 1)
        self._exp(SortMerge(), 3, 2)
