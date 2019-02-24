import unittest

from DBObject.Buffer import Buffer
from DBObject.DataFile import DataFile
from DBObject.Table import Table
from Algorithm.NestedLoop import NestedLoop
from Algorithm.BlockNestedLoop import BlockNestedLoop
from Algorithm.SortMerge import SortMerge
from Operator import Join
from Benchmark.Counter import Counter
from Benchmark.MeasurerProxy import MeasurerProxy
from Utility.Parameterization import Parametrization
from Utility.JointsGenerator import JointsGenerator
import math


class JointsGeneratorTest(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self.params = Parametrization()
        self.params.SetSelectivity(0.1).SetBufferSize(100,n=5).SetSize(50).recalculate()
        self.generator = JointsGenerator(self.params.GetTotalSize(), self.params.GetGoodDataSize())

    def _exp(self,algorithm):
        B_R = self.params.GetRSize()
        B_S = self.params.GetSSize()

        M = self.params.GetBufferSize()
        expected = B_R * B_S * (self.params.GetBlockSize() ** 2)

        counter = Counter()
        counter.Observe("NextBlock")
        counter.Observe("LoadBlockWith")

        buffer = Buffer(M)
        fR = DataFile(B_R, key_size=self.params.GetRKeySize(), block_size=self.params.GetBlockSize(), name="fR")
        fS = DataFile(B_S, key_size=self.params.GetSKeySize(), block_size=self.params.GetBlockSize(), name="fS")
        fR = MeasurerProxy(fR, counter, name="fR")
        fS = MeasurerProxy(fS, counter, name="fS")

        R = Table(fR, buffer.GetMemorySpace(1))
        S = Table(fS, buffer.GetMemorySpace(100))

        self.assertEqual(B_R, R.GetSize(), "Size of R")
        self.assertEqual(B_S, S.GetSize(), "Size of S")

        algorithm.join(R, S, self.generator.condition)

        self.assertEqual(round(self.params.RealSelectivity(), 2), round(algorithm.GetOutputSize() / expected, 2),
                         "Output size")

    def _test_nested_loop(self):
        self._exp(NestedLoop())

    def test_block_nested_loop(self):
        self._exp(BlockNestedLoop())

    def test_sort_merge(self):
        self._exp(SortMerge())
