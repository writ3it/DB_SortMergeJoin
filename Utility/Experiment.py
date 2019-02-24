import numpy as np
import math
from DBObject.Buffer import Buffer
from DBObject.DataFile import DataFile
from DBObject.Table import Table
from Benchmark.Counter import Counter
from Benchmark.MeasurerProxy import MeasurerProxy
from Utility.JointsGenerator import JointsGenerator
from Utility.Parameterization import Parametrization
import csv
import datetime
import os


class Experiment:

    def __init__(self, name:str):

        self.bufferRange = [1,10, 1]
        self.constBuffer = False
        self.splitBuffer = False
        self.tableSize = 50
        self.blockSize = 5
        min_sel = 1 / (self.tableSize*self.blockSize)
        self.selectivityRange = [min_sel, 1, 10]
        self.algorithm = None
        self.name = name
        self.data = []

    def SetSelectivityRange(self, start: float, stop: float, steps: int):
        self.selectivityRange = [start, stop, steps]
        return self

    def SetBufferRange(self, start: int, stop: int, steps: int):
        self.bufferRange = [start, stop, steps]
        return self

    def SetBlockSize(self, block_size: int):
        self.blockSize = block_size
        return self

    def SetConstRBufferSize(self, bufferSize: int):
        if self.splitBuffer:
            raise Exception('You can use one Buffer plan!')
        self.constBuffer = bufferSize
        return self

    def SetAlgorithm(self, algoName: str):
        m = __import__("Algorithm."+algoName)
        m = getattr(m, algoName)
        self.algorithm = getattr(m, algoName)
        return self

    def SetConstBufferSplit(self, r_factor: float):
        if self.constBuffer:
            raise Exception('You can use one Buffer plan!')
        self.splitBuffer = r_factor
        return self

    def Out(self,line:list):
        self.data.append(line)

    def Run(self):
        self.Out(["Rozmiar bloku: ", self.blockSize, "Nazwa", self.name])
        line = ["\/ Rozmiar bufora (bloki) / selektywność =>"]
        for selectivity in np.linspace(*self.selectivityRange):
            line.append(selectivity)

        total = self.bufferRange[2] * self.selectivityRange[2]
        i = 0
        for buffer_size in np.linspace(*self.bufferRange):
            bs = int(buffer_size)
            line = [bs]
            for selectivity in np.linspace(*self.selectivityRange):
                algo = self.algorithm()
                params = Parametrization()
                params.SetSelectivity(selectivity)\
                    .SetBufferSize(bs, n=self.blockSize)\
                    .SetSize(self.tableSize)\
                    .recalculate()
                generator = JointsGenerator(params.GetTotalSize(), params.GetGoodDataSize())
                progress = math.ceil((i / total)*100)
                self.SetBuffers(params, bs)
                print("Progress= "+str(progress)+"% | Run bs="+str(bs)+" selectivity="+str(selectivity) +" RBuffer="+str(params.GetRBufferSize())+" SBuffer="+str(params.GetSBufferSize()))
                value = self.exp(algo, params, generator)
                i += 1
                line.append(value[0])
            self.Out(line)
        self.Dump()

    def SetBuffers(self, params: Parametrization, bs: int):
        if self.constBuffer:
            print("Const split " + str(self.constBuffer))
            params.SetRBufferSize(self.constBuffer)
        if self.splitBuffer:
            print("Var split "+str(self.splitBuffer))
            params.SetRBufferSize(math.floor(bs * self.splitBuffer))
        params.SetSBufferSize(bs - params.GetRBufferSize())

    def Dump(self):
        d = datetime.datetime.now()
        dt = '{:%Y-%m-%d}'.format(d)
        path = os.getcwd()+"/output/"+self.name+"-"+dt+".csv"
        with open(path, "wb"):
            writer = csv.writer(f)
            writer.writerows(self.data)

    def exp(self, algorithm, params: Parametrization, generator: JointsGenerator):
        B_R = params.GetRSize()
        B_S = params.GetSSize()

        counter = Counter()
        counter.Observe("NextBlock")
        counter.Observe("LoadBlockWith")

        buffer = Buffer(params.GetBufferSize())
        fR = DataFile(B_R, key_size=params.GetRKeySize(), block_size=params.GetBlockSize(), name="fR")
        fS = DataFile(B_S, key_size=params.GetSKeySize(), block_size=params.GetBlockSize(), name="fS")
        fR = MeasurerProxy(fR, counter, name="fR")
        fS = MeasurerProxy(fS, counter, name="fS")

        R = Table(fR, buffer.GetMemorySpace(params.GetRBufferSize()))
        S = Table(fS, buffer.GetMemorySpace(params.GetSBufferSize()))

        algorithm.join(R, S, generator.condition)

        return [counter.GetValue(), algorithm.GetOutputSize()]


