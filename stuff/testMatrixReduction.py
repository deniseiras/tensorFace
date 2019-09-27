
import numpy as np
A = np.matrix([
    [1,1,2,2,3],
    [1,1,2,2,3],
    [4,4,5,5,6],
    [4,4,5,5,6],
    [7,7,8,8,9],
    # [7,7,8,8,9,9]
])
N, M = A.shape
k = 2
# assert N % k == 0
# assert M % k == 0
A1 = np.empty((N // k, M // k))
A2 = np.empty((N // k, M // k))
for i in range(N // k):
    for j in range(M // k):
         A1[i,j] = A[k*i:k*i+k, k*j:k*j+k].mean()
         # A2[i,j] = A1[i, j]/(k*k)



print(A.mean())
print(A1)
print(A1 * 2)
# print(A2)