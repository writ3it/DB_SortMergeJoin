import unittest
from Algorithm.SortMerge import SortMerge
from DBObject.Buffer import Buffer
from DBObject.BufferedFile import BufferedFile


class SortMergeTestCase(unittest.TestCase):


    def test_run(self):
        bs = 100
        buffer = Buffer(noBlocks=100, blockSize=bs)
        R = BufferedFile(buffer, size=50*bs, valueSize=1)
        S = BufferedFile(buffer, size=500*bs, valueSize=10)
        algo = SortMerge(R,S)
        algo.Run()

        print("T="+str(algo.GetExecutionEstimation()))
        print("T[R] ="+str(R.GetCounterVal(BufferedFile.COUNTER_DISK_READS)))
        print("T[S] =" + str(S.GetCounterVal(BufferedFile.COUNTER_DISK_READS)))

        self.assertEqual(50, R.GetCounterVal(BufferedFile.COUNTER_DISK_READS))
        self.assertEqual(500, S.GetCounterVal(BufferedFile.COUNTER_DISK_READS))


if __name__ == '__main__':
    unittest.main()