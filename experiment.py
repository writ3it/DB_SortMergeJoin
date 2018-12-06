from Algorithm.SortMerge import SortMerge
from DBObject.Buffer import Buffer
from DBObject.BufferedFile import BufferedFile

from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter
import numpy as np


def experiment(M:int, L:int,pr:float, ps:float, n:int = 100):
    bs = L
    print("Buffer: number of blocks = "+str(M)+" block size = "+str(bs))
    buffer = Buffer(noBlocks=M, blockSize=bs)
    RValSize = int(pr*M*L)
    SValSize = int(ps*M*L)

    N = n*n*n*n
    vn = np.sqrt(N/(RValSize*SValSize))
    RSize = int(RValSize * vn)
    SSize = int(SValSize * vn)
    print("R: number of blocks = " + str(RSize / bs) + " val size (rows) = " + str(RValSize))
    print("S: number of blocks = " + str(SSize / bs) + " val size (rows) = " + str(SValSize))
    R = BufferedFile(buffer, size=RSize, valueSize=RValSize)
    S = BufferedFile(buffer, size=SSize, valueSize=SValSize)
    algo = SortMerge(R, S)
    algo.Run()
    return algo.GetExecutionEstimation()


def run_experiment(pr,ps):
    output = np.zeros(pr.shape)
    for i in range(0, pr.shape[0]):
        for j in range(0, pr.shape[1]):
            ipr = pr[i][j]
            ips = ps[i][j]
            output[i][j] = experiment(10,10,ipr, ips)
    return output


fig = plt.figure()
ax = fig.gca(projection='3d')

PR = np.arange(0.01, 1.51,0.2)
PS = np.arange(0.01, 1.51,0.2)
X, Y = np.meshgrid(PR, PS)


Z = run_experiment(X,Y)

surf = ax.plot_surface(X, Y, Z, cmap=cm.coolwarm,
                       linewidth=0, antialiased=False)
ax.zaxis.set_major_locator(LinearLocator(10))
ax.zaxis.set_major_formatter(FormatStrFormatter('%.02f'))

# Add a color bar which maps values to colors.
fig.colorbar(surf, shrink=0.5, aspect=5)

plt.show()