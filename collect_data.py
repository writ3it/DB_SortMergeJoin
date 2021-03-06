import random
from Utility.Experiment import Experiment
import math

# experiment has to be recurrent
random.seed(23)


def ConstBuffer(name: str, algoName: str):
    sortMerge = Experiment(name)
    blocks = 100
    max_blocks = blocks // 3
    block = 10
    sel = 0.02
    print("Max sel = "+str(sel))

    sortMerge.SetAlgorithm(algoName) \
        .SetTableSize(blocks) \
        .SetBlockSize(block) \
        .SetSelectivityRange(0, sel, 30) \
        .SetBufferRange(2, max_blocks, 10)
    return sortMerge

ConstBuffer("SortMerge-sbuffer", "SortMerge").SetConstSBufferSize(1).Run()
ConstBuffer("CalcNestedLoop-sbuffer", "CalcNestedLoop").SetConstSBufferSize(1).Run()

ConstBuffer("SortMerge", "SortMerge").SetConstRBufferSize(1).Run()
ConstBuffer("CalcNestedLoop", "CalcNestedLoop").SetConstRBufferSize(1).Run()

ConstBuffer("SortMerge-split", "SortMerge").SetConstBufferSplit(0.5).Run()
ConstBuffer("CalcNestedLoop-split", "CalcNestedLoop").SetConstBufferSplit(0.5).Run()






