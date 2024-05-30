import numpy as np

def Clip3(x, y, z):
    if z < x:
        return x
    if z > y:
        return y
    return z

def Cliplyc(x, bitDepthyc):
    return Clip3(0, (1<< bitDepthyc)-1, x)

ZIG_ZAG_4x4_MAP = [
    [0, 0],[0,1], [1,0], [2,0], [1, 1], [0, 2], [0, 3], [1, 2], [2, 1], [3, 0], [ 3, 1], [2, 2], [1, 3], [2, 3], [3, 2], [3, 3]
]

def inverse_scanning_4x4_transform_coeff(list:np.array):
    c = np.zeros(shape=(4,4), dtype=np.int32)
    for i in range(16):
        x, y  = ZIG_ZAG_4x4_MAP[i][0], ZIG_ZAG_4x4_MAP[i][1]
        c[x][y] = list[i]
    return c

def weightScale4x4():
    flat_4x4 = [16]*16
    return inverse_scanning_4x4_transform_coeff(flat_4x4)

def LevelScale4x4(m, i, j):
    return weightScale4x4()[i][j] * normAdjust4x4(m, i, j)


V = [
    [10, 16, 13],
    [11, 18, 14],
    [13, 20, 16],
    [14, 23, 18],
    [16, 25, 20],
    [18, 29, 23]
]

def normAdjust4x4(m, i, j):
    if i%2 == 0 and j %2 == 0:
        return V[m][0]
    if i%2 == 1 and j %2 == 1:
        return V[m][1]
    return V[m][2]
