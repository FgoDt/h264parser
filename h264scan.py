import math

def InverseRasterScan(a, b, c, d, e):
    if e == 0:
        return (a%(d//b))*b
    elif e == 1:
        return (a//(d//b))*c
    else:
        assert False

#6.4.3
def inverse_4x4_luma_block_scanning_process(idx):
    x = InverseRasterScan(idx//4, 8, 8, 16, 0) + InverseRasterScan(idx%4, 4, 4, 8, 0)
    y = InverseRasterScan(idx//4, 8, 8, 16, 1) + InverseRasterScan(idx%4, 4, 4, 8, 1)
    return (x, y)

def derivation_process_neighbouring_4x4_luma_blocks(idx):
    pass

#6.4.9 and 6.4.10
def derivation_process_neighbouring_macroblock_addr(MBAFF:bool, curr:int, PicWidthInMbs):
    mba = -1
    mbb = -1
    mbc = -1
    mbd = -1
    if not MBAFF:
        if curr % PicWidthInMbs != 0:
            mba = curr - 1
        mbb = curr - PicWidthInMbs
        if (curr+1)%PicWidthInMbs != 0:
            mbc = curr - PicWidthInMbs + 1
        if curr % PicWidthInMbs != 0:
            mbd = curr - PicWidthInMbs - 1
    else:
        if (curr//2)%PicWidthInMbs != 0:
            mba = 2 *(curr//2 -1)
        mbb = 2 * ( curr//2 - PicWidthInMbs)
        if (curr/2 + 1) % PicWidthInMbs != 0:
            mbc = 2*(curr//2 - PicWidthInMbs + 1)
        if (curr//2)%PicWidthInMbs != 0:
            mbd = 2 (curr//2 - PicWidthInMbs -1)
    return (mba, mbb, mbc, mbd)

#6.4.11
for i in range(16):
    print(inverse_4x4_luma_block_scanning_process(i))