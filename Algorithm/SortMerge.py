from DBObject.BufferedFile import BufferedFile
from typing import Callable
from DBObject.RowAccess import RowAccess
import numpy as np

from DBObject.Buffer import Buffer

def log(str):
    #print(str)
    pass

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
        log("R id = "+str(id(self.R)))
        S = RowAccess(self.S)
        log("S id = " + str(id(self.S)))
        col="A"
        # order is important for easies way to calculate expected values in tests
        R.readRow()
        S.readRow()
        finished = False
        while True:
            y = self.findMinimumValue(R,S,y)
            log("y = "+str(y))
            if (y is False):
                break
            S.savePosition()
            while R.current(col) == y:
                log("Rloop")
                while S.current(col) == y:
                    row = {"R":R.current(), "S": S.current()}
                    log(row)
                    if S.eof():
                        log("S break")
                        break
                    log("S read")
                    S.readRow()
                if R.eof():
                    log("R break")
                    break
                log("R read")
                if R.eof():
                    log("R break")
                    finished = True
                    break
                R.readRow()
                if R.current(col) == y:
                    log("S rewind")
                    S.restorePosition()
        if finished:
            return True


    def findMinimumValue(self,R:RowAccess,S:RowAccess,y,col="A"):
        r = R.current(col)
        log("r <= y "+str(r)+" <= "+str(y))
        while r <= y:
            if R.eof():
                return False
            R.readRow()
            r = R.current(col)

        s = S.current(col)
        log("s <= y " + str(s) + " <= " + str(y))
        while s <= y:
            if S.eof():
                return False
            S.readRow()
            s = S.current(col)

        if (r<s):
            return self.findMinimumValue(R,S,s)

        if (s<r):
            return self.findMinimumValue(R,S,r)

        return r





    def GetExecutionEstimation(self):
        return self.R.GetCounterVal(BufferedFile.COUNTER_DISK_READS) + self.S.GetCounterVal(BufferedFile.COUNTER_DISK_READS)
