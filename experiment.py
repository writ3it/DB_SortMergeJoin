from Algorithm.SortMerge import SortMerge
from Algorithm.NestedLoop import NestedLoop
from DBObject.Buffer import Buffer
from DBObject.BufferedFile import BufferedFile

from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter
import numpy as np


def experiment(M:int, L:int,pr:float, ps:float, n:int = 100, callback=False):
    bs = L
    print("Buffer: number of blocks = "+str(M)+" block size = "+str(bs))

    RValSize = int(pr*M*L)
    SValSize = int(ps*M*L)

    targetF = 2000

    RSize = int(targetF / (RValSize + SValSize) * RValSize)
    SSize = int(targetF / (RValSize + SValSize) * SValSize)

    #N = n*n*n*n
    #vn = np.sqrt(N/(RValSize*SValSize))
    #RSize = int(RValSize * vn)
    #SSize = int(SValSize * vn)
    print("RValueSize = "+str(RValSize)+" SValueSize = "+str(SValSize))
    print("R: number of blocks = " + str(int(RSize / bs)) + " val size (rows) = " + str(RValSize) + " pr = "+str(pr))
    print("S: number of blocks = " + str(int(SSize / bs)) + " val size (rows) = " + str(SValSize)+ " ps = "+str(ps) )
    print("Sum of blocks " + str(int(RSize/bs) + int(SSize/bs)))
    return callback(M, bs, RSize, SSize, RValSize, SValSize)


def sortmerge(M:int, bs:int, RSize:int, SSize:int, RValSize:int, SValSize:int):
    buffer = Buffer(noBlocks=M, blockSize=bs)
    R = BufferedFile(buffer, size=RSize, valueSize=RValSize)
    S = BufferedFile(buffer, size=SSize, valueSize=SValSize)
    algo = SortMerge(R, S)
    algo.Run()
    return algo.GetExecutionEstimation() + 4 * ( int(RSize/bs) + int(SSize/bs))

def nestedloop(M:int, bs:int, RSize:int, SSize:int, RValSize:int, SValSize:int):
    buffer = Buffer(noBlocks=M, blockSize=bs)
    R = BufferedFile(buffer, size=RSize, valueSize=RValSize)
    S = BufferedFile(buffer, size=SSize, valueSize=SValSize)
    algo = NestedLoop(R, S)
    algo.Run()
    return algo.GetExecutionEstimation()




def run_experiment(pr,ps, callback):
    output = np.zeros(pr.shape)
    for i in range(0, pr.shape[0]):
        for j in range(0, pr.shape[1]):
            ipr = pr[i][j]
            ips = ps[i][j]
            output[i][j] = experiment(10,10,ipr, ips,callback=callback)
    return output


fig = plt.figure(1)
fig.suptitle("SortMerge")
ax = fig.gca(projection='3d')

PR = np.arange(0.01, 1.51,0.2)
PS = np.arange(0.01, 1.51,0.2)
X, Y = np.meshgrid(PR, PS)


Z = run_experiment(X,Y, sortmerge)

surf = ax.plot_surface(X, Y, Z, cmap=cm.coolwarm,
                       linewidth=0, antialiased=False)
ax.zaxis.set_major_locator(LinearLocator(10))
ax.zaxis.set_major_formatter(FormatStrFormatter('%.02f'))
ax.set_xlabel("PR")
ax.set_xlabel("PS")

# Add a color bar which maps values to colors.
fig.colorbar(surf, shrink=0.5, aspect=5)


print("###############################")
print("###############################")
print("###############################")
print("###############################")
print("###############################")
print("###############################")
print("###############################")
print("###############################")

fig = plt.figure(2)
fig.suptitle("Nestedloop")
ax = fig.gca(projection='3d')

PR = np.arange(0.01, 1.51,0.2)
PS = np.arange(0.01, 1.51,0.2)
X, Y = np.meshgrid(PR, PS)


Z2 = run_experiment(X,Y, nestedloop)

surf = ax.plot_surface(X, Y, Z2, cmap=cm.coolwarm,
                       linewidth=0, antialiased=False)
ax.zaxis.set_major_locator(LinearLocator(10))
ax.zaxis.set_major_formatter(FormatStrFormatter('%.02f'))
ax.set_xlabel("PR")
ax.set_xlabel("PS")

# Add a color bar which maps values to colors.
fig.colorbar(surf, shrink=0.5, aspect=5)


fig = plt.figure(3)
fig.suptitle("Nestedloop - SortMerge ")
ax = fig.gca(projection='3d')

PR = np.arange(0.01, 1.51,0.2)
PS = np.arange(0.01, 1.51,0.2)
X, Y = np.meshgrid(PR, PS)


Z = Z2 - Z
ax.plot_surface(X, Y, np.zeros((len(PR),len(PS))), alpha=0.2)
surf = ax.plot_surface(X, Y, Z, cmap=cm.coolwarm,
                       linewidth=0, antialiased=False)

ax.zaxis.set_major_locator(LinearLocator(10))
ax.zaxis.set_major_formatter(FormatStrFormatter('%.02f'))
ax.set_xlabel("PR")
ax.set_xlabel("PS")

# Add a color bar which maps values to colors.
fig.colorbar(surf, shrink=0.5, aspect=5)

plt.show()