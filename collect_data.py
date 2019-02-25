import random
from Utility.Experiment import Experiment
import math

# experiment has to be recurrent
random.seed(23)


def ConstBuffer(name: str, algoName: str):
    sortMerge = Experiment(name)
    blocks = 100
    max_blocks = blocks // 2
    block = 10
    rows = max_blocks * block
    rows2 = blocks*block
    sel = rows2/(rows2**2)
    print("Max sel = "+str(sel))

    sortMerge.SetAlgorithm(algoName) \
        .SetTableSize(blocks) \
        .SetBlockSize(block) \
        .SetSelectivityRange(0, sel, 30) \
        .SetBufferRange(2, max_blocks, 10)
    return sortMerge


ConstBuffer("SortMerge", "SortMerge").SetConstRBufferSize(1).Run()
ConstBuffer("BlockNestedLoop", "BlockNestedLoop").SetConstRBufferSize(1).Run()

ConstBuffer("SortMerge-split", "SortMerge").SetConstBufferSplit(0.5).Run()
ConstBuffer("BlockNestedLoop-split", "BlockNestedLoop").SetConstBufferSplit(0.5).Run()




