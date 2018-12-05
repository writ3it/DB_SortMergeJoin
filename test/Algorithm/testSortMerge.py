import unittest
import logging
from Algorithm.SortMerge import SortMerge
from DBObject.Buffer import Buffer
from DBObject.BufferedFile import BufferedFile


class SortMergeTestCase(unittest.TestCase):


    def test_reads_in_buffer(self):
        self.simple_test(noBlocks=100, blockSize=100, RSize=50 * 100, SSzie=500 * 1000, RValSize=1, SValSize=10, expectedR=50, expectedS=500)
        self.simple_test(noBlocks=100, blockSize=100, RSize=50*100, SSzie=500*1000, RValSize=1,SValSize=10, expectedR=50, expectedS=500)
        self.simple_test(noBlocks=100, blockSize=100, RSize=50 * 100, SSzie=500 * 1000, RValSize=2, SValSize=10, expectedR=50, expectedS=500)
        self.simple_test(noBlocks=100, blockSize=100, RSize=50 * 100, SSzie=500 * 1000, RValSize=10, SValSize=10, expectedR=50, expectedS=500)
        self.simple_test(noBlocks=100, blockSize=100, RSize=50 * 100, SSzie=500 * 1000, RValSize=99, SValSize=10, expectedR=50, expectedS=500)
        self.simple_test(noBlocks=100, blockSize=100, RSize=50 * 100, SSzie=500 * 1000, RValSize=100, SValSize=10, expectedR=50, expectedS=500)
        self.simple_test(noBlocks=100, blockSize=100, RSize=50 * 100, SSzie=500 * 1000, RValSize=100, SValSize=100, expectedR=50, expectedS=500)




    def simple_test(self, noBlocks, blockSize, RSize, SSzie, RValSize, SValSize, expectedR, expectedS):
        log = logging.getLogger("SimpleTest.SortMerge")
        bs = blockSize
        buffer = Buffer(noBlocks=noBlocks, blockSize=bs)
        R = BufferedFile(buffer, size=50 * bs, valueSize=1)
        S = BufferedFile(buffer, size=500 * bs, valueSize=10)
        algo = SortMerge(R, S)
        algo.Run()

        #print("T=" + str(algo.GetExecutionEstimation()))
        #print("T[R] =" + str(R.GetCounterVal(BufferedFile.COUNTER_DISK_READS)))
        #print("T[S] =" + str(S.GetCounterVal(BufferedFile.COUNTER_DISK_READS)))

        self.assertEqual(expectedR, R.GetCounterVal(BufferedFile.COUNTER_DISK_READS))
        self.assertEqual(expectedS, S.GetCounterVal(BufferedFile.COUNTER_DISK_READS))


if __name__ == '__main__':
    unittest.debug(True)