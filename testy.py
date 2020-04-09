import numpy as np


n = int(input())
mat = []
ans = []
for i in range(n):
    a = list(map(int, input().split()))
    mat.append(a[:-1])
    ans.append(a[-1])

mat = np.array(mat)
ans = np.array(ans)

print(np.linalg.solve(mat, ans))
