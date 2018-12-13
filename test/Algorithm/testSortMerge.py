import unittest
import logging
from Algorithm.SortMerge import SortMerge
from DBObject.Buffer import Buffer
from DBObject.BufferedFile import BufferedFile
from DBObject.RowAccess import RowAccess
import numpy as np


class SortMergeTestCase(unittest.TestCase):


    def test_reads_in_buffer(self):
        print("test_reads_in_buffer")
        self.simple_test(noBlocks=100, blockSize=100, RSize=50 * 100, SSize=500 * 100, RValSize=1, SValSize=10, expectedR=50, expectedS=500,testName= "1x10")
        self.simple_test(noBlocks=100, blockSize=100, RSize=50 * 100, SSize=250 * 100, RValSize=2, SValSize=10, expectedR=50, expectedS=250,testName= "2x10")
        self.simple_test(noBlocks=100, blockSize=100, RSize=50 * 100, SSize=50 * 100, RValSize=10, SValSize=10, expectedR=50, expectedS=50,testName= "10x10")
        self.simple_test(noBlocks=100, blockSize=100, RSize=99 * 100, SSize=10 * 100, RValSize=99, SValSize=10, expectedR=99, expectedS=10, testName="99x10")
        # one block more is needed because one relation fill whole buffer and second should be reloaded
        self.simple_test(noBlocks=100, blockSize=100, RSize=100 * 100, SSize=10 * 100, RValSize=100, SValSize=10, expectedR=100, expectedS=10,testName= "100x10")
        # still one block more because buffer is FIFO (reloaded block is newest)
        self.simple_test(noBlocks=100, blockSize=100, RSize=100 * 100, SSize=100 * 100, RValSize=100, SValSize=100, expectedR=100, expectedS=100,testName= "100x100")


    def test_reads_S_out_of_buffer(self):
        print("test_reads_S_out_of_buffer")
        # coś chyba w rekurencji nie chula
        self.simple_test(noBlocks=10, blockSize=100, RSize=2 , SSize=1200 * 100, RValSize=1, SValSize=600*100, expectedR=1, expectedS=1200,testName= "1x1200")

    def test_reads_R_out_of_buffer(self):
        print("test_reads_R_out_of_buffer")
        self.simple_test(noBlocks=10, blockSize=100, RSize=1200*100, SSize=2, RValSize=600*100, SValSize=1,
                         expectedR=1200, expectedS=120, testName="1200x1")


    def test_findMin(self):
        buffer = Buffer(noBlocks=10, blockSize=10)
        fR = BufferedFile(buffer, size=100, valueSize=1)
        fS = BufferedFile(buffer, size=1000, valueSize=10)
        algo = SortMerge(fR, fS)
        y = -np.inf
        R = RowAccess(fR)
        S = RowAccess(fS)
        R.readRow()
        S.readRow()
        for i in range(100):
            y = algo.findMinimumValue(R,S,y)
            self.assertEqual(i,y)
        self.assertEqual(10, fR.GetCounterVal(BufferedFile.COUNTER_DISK_READS))
        self.assertEqual(100, fS.GetCounterVal(BufferedFile.COUNTER_DISK_READS))



    def simple_test(self, noBlocks, blockSize, RSize, SSize, RValSize, SValSize, expectedR, expectedS,testName):
        log = logging.getLogger("SimpleTest.SortMerge")
        bs = blockSize
        buffer = Buffer(noBlocks=noBlocks, blockSize=bs)
        R = BufferedFile(buffer, size=RSize, valueSize=RValSize)
        S = BufferedFile(buffer, size=SSize, valueSize=SValSize)
        algo = SortMerge(R, S)
        algo.Run()
      #  print("T=" + str(algo.GetExecutionEstimation()))
       # print("T[R] =" + str(R.GetCounterVal(BufferedFile.COUNTER_DISK_READS)))
      #  print("T[S] =" + str(S.GetCounterVal(BufferedFile.COUNTER_DISK_READS)))
        testName = testName + " Seek R=" + str(S.GetCounterVal(BufferedFile.COUNTER_SEEK)) +"  Seek S=" + str(S.GetCounterVal(BufferedFile.COUNTER_SEEK))
        self.assertEqual(expectedR, R.GetCounterVal(BufferedFile.COUNTER_DISK_READS), msg="R: "+testName)
        self.assertEqual(expectedS, S.GetCounterVal(BufferedFile.COUNTER_DISK_READS), msg="S: "+testName)


if __name__ == '__main__':
    unittest.debug(True)