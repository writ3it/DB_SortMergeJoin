import unittest

class NestedLoopTestCase(unittest.TestCase):


    def test_disk_accesses(self):
        B_R = 1000
        B_S = 500
        M = 101
        expected_L = 5500
        expected_R = 6000

        buffer = Buffer(M)
        fR = DataFile(B_R,1)
        fS = DataFile(B_S,1)

        R = Table(fR, buffer.GetMemorySpace(1))
        S = Table(fS, buffer.GetMemorySpace(100))

        algorithm = NestedLoop()
        algorithm.join(R,S,Join.EQUAL)

        actual = buffer.GetDiskHitsCounter()
        self.assertEqual(expectedL, actual, "Join R->S")

        buffer.ResetCoutners()
        algorithm = NestedLoop()
        algorithm.join(S, R, Join.EQUAL)

        actual = buffer.GetDiskHitsCounter()
        self.assertEqual(expected_R, actual, "Join S->R")


