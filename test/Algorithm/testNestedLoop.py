import unittest
import logging
from Algorithm.NestedLoop import NestedLoop
from DBObject.Buffer import Buffer
from DBObject.BufferedFile import BufferedFile
from DBObject.RowAccess import RowAccess
import numpy as np


class SortMergeTestCase(unittest.TestCase):


    def test_reads_in_buffer(self):
        print("test_reads_in_buffer")
       # self.simple_test(noBlocks=10, blockSize=1, RSize=10, SSize=10, RValSize=1, SValSize=1, expectedR=10, expectedS=11,testName="10x10")
        self.simple_test(noBlocks=2, blockSize=2, RSize=20, SSize=20, RValSize=5, SValSize=5, expectedR=5,
                         expectedS=25, testName="5x5")




    def simple_test(self, noBlocks, blockSize, RSize, SSize, RValSize, SValSize, expectedR, expectedS,testName):
        log = logging.getLogger("SimpleTest.SortMerge")
        bs = blockSize
        buffer = Buffer(noBlocks=noBlocks, blockSize=bs)
        R = BufferedFile(buffer, size=RSize, valueSize=RValSize)
        S = BufferedFile(buffer, size=SSize, valueSize=SValSize)
        algo = NestedLoop(R, S)
        algo.Run()
      #  print("T=" + str(algo.GetExecutionEstimation()))
       # print("T[R] =" + str(R.GetCounterVal(BufferedFile.COUNTER_DISK_READS)))
      #  print("T[S] =" + str(S.GetCounterVal(BufferedFile.COUNTER_DISK_READS)))
        testName = testName + " Seek R=" + str(S.GetCounterVal(BufferedFile.COUNTER_SEEK)) +"  Seek S=" + str(S.GetCounterVal(BufferedFile.COUNTER_SEEK))
        self.assertEqual(expectedR, R.GetCounterVal(BufferedFile.COUNTER_DISK_READS), msg="R: "+testName)
        self.assertEqual(expectedS, S.GetCounterVal(BufferedFile.COUNTER_DISK_READS), msg="S: "+testName)


if __name__ == '__main__':
    unittest.debug(True)