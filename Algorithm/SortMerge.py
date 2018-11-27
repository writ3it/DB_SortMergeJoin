from DBObject.BufferedFile import BufferedFile
from typing import Callable

class SortMerge:

    '''
    leftRelation - BufferedFile
    rightRelation - BufferedFile
    condition - lambda a,b: a == b
    '''
    def __init__(self, leftRelation:BufferedFile, rightRelation:BufferedFile, condition: Callable[[int,int],bool]):
        pass