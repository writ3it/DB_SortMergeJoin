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
        B_R = 1000
        B_S = 500
        M = 101
        expected_L = 5500
        expected_R = 6000

        counter = Counter()
        counter.Observe("NextBlock")

        buffer = Buffer(M)
        fR = DataFile(B_R,key_size=1, block_size=5)
        fS = DataFile(B_S,key_size=1, block_size=5)
        fR = MeasurerProxy(fR,counter)
        fS = MeasurerProxy(fS, counter)

        R = Table(fR, buffer.GetMemorySpace(1))
        S = Table(fS, buffer.GetMemorySpace(100))

        algorithm = NestedLoop()
        algorithm.join(R,S,Join.EQUAL)

        self.assertEqual(expected_L, counter.GetValue(), "Join R->S")



