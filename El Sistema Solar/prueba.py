import math
import numpy as np

A = np.array([[1,1],[2,2],[3,3]])

dist = np.empty((3,2,3,2))

np.subtract.outer(A, A, out=dist)

x,y = dist[2,0,1]

print(x,y)

# r[i]-r[j] = r[i,0,j]



