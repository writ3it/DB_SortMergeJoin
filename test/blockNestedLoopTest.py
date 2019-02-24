import unittest

from DBObject.Buffer import Buffer
from DBObject.DataFile import DataFile
from DBObject.Table import Table
from Algorithm.BlockNestedLoop import BlockNestedLoop
from Operator import Join
from Benchmark.Counter import Counter
from Benchmark.MeasurerProxy import MeasurerProxy

class BlockNestedLoopTest(unittest.TestCase):



    # Garcia-Molina example
    def test_disk_accesses(self):
        B_R = 1000
        B_S = 500
        M = 101
        expected = 5500 # rows(R) * blocks(S) + blocks(R)
        expected2 = 6000

        counter = Counter()
        counter.Observe("NextBlock")

        buffer = Buffer(M)
        fR = DataFile(B_R,key_size=1, block_size=5, name="fR")
        fS = DataFile(B_S,key_size=1, block_size=5, name="fS")
        fR = MeasurerProxy(fR, counter, name="fR")
        fS = MeasurerProxy(fS, counter, name="fS")

        R = Table(fR, buffer.GetMemorySpace(1))
        S = Table(fS, buffer.GetMemorySpace(100))

        self.assertEqual(B_R, R.GetSize(), "Size of R")
        self.assertEqual(B_S, S.GetSize(), "Size of S")

        algorithm = BlockNestedLoop()
        algorithm.join(R, S, Join.EQUAL)

        self.assertEqual(expected, counter.GetValue(), "Join R->S")

        counter.Reset()

        S = Table(fS, buffer.GetMemorySpace(1))
        R = Table(fR, buffer.GetMemorySpace(100))

        algorithm.join(S, R, Join.EQUAL)
        self.assertEqual(expected2, counter.GetValue(), "Join S->R")


