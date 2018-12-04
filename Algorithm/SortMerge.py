from DBObject.BufferedFile import BufferedFile
from typing import Callable
from DBObject.RowAccess import RowAccess
import numpy as np

class SortMerge:

    '''
    leftRelation - BufferedFile
    rightRelation - BufferedFile
    condition - lambda a,b: a == b

    assumption!
    Condition is an equality
    '''
    def __init__(self, leftRelation:BufferedFile, rightRelation:BufferedFile):
        self.R = leftRelation
        self.S = rightRelation
        pass


    def Run(self):
        # Step 1. Sort R, omitted
        # Step 2. Sort S, omitted
        y = -np.inf
        R = RowAccess(self.R)
        S = RowAccess(self.S)
        r = R.readRow()
        s = S.readRow()
        while True: #Step 3. Merge
            # Step. 3.a. find min y that exists in R & S

            y = self.findMinimumValue(R,r,S,s,y)
            if (y is False):
                break
            if (R.eof() or S.eof()):
                break
            R.savePosition()
            S.savePosition()

            while R.current(0) == y:
                S.restorePosition()
                while S.current(0) == y:
                    row = R.current()+S.current()
                    # Saving output to buffer is omitted
                    # print(row)
                    s = S.readRow()
                r = R.readRow()





    def findMinimumValue(self,R:RowAccess,r,S:RowAccess,s,y):

        if (R.eof() or S.eof()) and s[0] != r[0]:
            return False

        if (r[0] == s[0]):
            return r[0]

        elif (r[0]>s[0]):
            while (r[0]>s[0]):
                s = S.readRow()
            return self.findMinimumValue(R,r,S,s,y)
        elif (r[0]<s[0]):
            while (r[0]<s[0]):
                r = R.readRow()
            return self.findMinimumValue(R,r,S,s,y)



    def GetExecutionEstimation(self):
        return self.R.GetCounterVal(BufferedFile.COUNTER_DISK_READS) + self.S.GetCounterVal(BufferedFile.COUNTER_DISK_READS)
