import unittest

from DBObject.Buffer import Buffer
from DBObject.DataFile import DataFile
from DBObject.Table import Table
from Algorithm.NestedLoop import NestedLoop
from Operator import Join
from Benchmark.Counter import Counter
from Benchmark.MeasurerProxy import MeasurerProxy

class NestedLoopTest(unittest.TestCase):


    def test_disk_accesses(self):
        B_R = 500
        B_S = 1000
        M = 101
        expected = 2500500 # rows(R) * blocks(S) + blocks(R)

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

        algorithm = NestedLoop()
        algorithm.join(R, S, Join.EQUAL)

        self.assertEqual(expected, counter.GetValue(), "Join R->S")
