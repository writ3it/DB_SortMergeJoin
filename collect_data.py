import random
from Utility.Experiment import Experiment


# experiment has to be recurrent
random.seed(23)

def ConstBuffer(name: str, algoName: str):
    sortMerge = Experiment(name)
    sortMerge.SetAlgorithm(algoName) \
        .SetTableName(100) \
        .SetBlockSize(10) \
        .SetSelectivityRange(0, 0.001, 30) \
        .SetBufferRange(2, 30, 10)
    return sortMerge


ConstBuffer("CalcNestedLoop", "CalcNestedLoop").SetConstRBufferSize(1).Run()
ConstBuffer("SortMerge", "SortMerge").SetConstRBufferSize(1).Run()
ConstBuffer("CalcNestedLoop-split", "CalcNestedLoop").SetConstBufferSplit(0.5).Run()
ConstBuffer("SortMerge-split", "SortMerge").SetConstBufferSplit(0.5).Run()



