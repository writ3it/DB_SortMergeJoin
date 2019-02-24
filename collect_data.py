import random
from Utility.Experiment import Experiment


# experiment has to be recurrent
random.seed(23)


sortMerge = Experiment("SortMergeJoin")
sortMerge.SetAlgorithm("SortMerge")\
            .SetBlockSize(5)\
            .SetSelectivityRange(0, 1, 10)\
            .SetBufferRange(2, 10, 8)\
            .SetConstRBufferSize(1)

sortMerge.Run()
