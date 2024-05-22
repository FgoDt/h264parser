import math
import h264_sps

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

#6.4.9
def neighbouring_macroblock_addr(curr, n):
    if n == "A":
        mbAddrA = curr - 1

#6.4.12
def neighbouring_locations(xN, yN, luma=True):
    maxW = maxH = 16

    mbAddrN = None

    if not luma:
        maxW = h264sps.MbWidthC(sps)
        maxH = h264sps.MbHeightC(sps)
    if MbaffFrameFlag == 0:
        if xN < 0 and yN < 0 :
            mbAddrN = 'mbAddrD'

        elif xN < 0 and  yN < maxH and yN >= 0 :
            mbAddrN = 'mbAddrA'
        elif xN>=0 and xN < maxW and  yN < 0:
            mbAddrN = 'mbAddrB'
        elif xN>=0 and xN < maxW and  yN >=0 and yN < maxH:
            mbAddrN = 'CurrMbAddr'
        elif xN >= maxW and yN < 0:
            mbAddrN = 'mbAddrC'
        else:
            mbAddrN = "not available"
    else :
        raise Exception("NOT IMP")
        
        xW = -1
        yW = -1
        if mbAddrN == 'not available':
            return None
        else:
            xW = (xN+maxW)%maxW
            yW = (yN+maxH)%maxH
            idx = luma_block_indices_4x4(xW, yW)
            return idx


def derivation_process_neighbouring_4x4_luma_blocks(idx, xD, yD, luma=True, sps=None, MbaffFrameFlag = 0):
    xy = inverse_4x4_luma_block_scanning_process(idx)
    xN = xy[0] + xD
    yN = xy[1] + yD
    maxW = maxH = 16

    mbAddrN = "not available"

    if not luma:
        maxW = h264sps.MbWidthC(sps)
        maxH = h264sps.MbHeightC(sps)
    if MbaffFrameFlag == 0:
        if xN < 0 and yN < 0 :
            mbAddrN = 'mbAddrD'
        elif xN < 0 and  yN < maxH and yN >= 0 :
            mbAddrN = 'mbAddrA'
        elif xN>=0 and xN < maxW and  yN < 0:
            mbAddrN = 'mbAddrB'
        elif xN>=0 and xN < maxW and  yN >=0 and yN < maxH:
            mbAddrN = 'CurrMbAddr'
        elif xN >= maxW and yN < 0:
            mbAddrN = 'mbAddrC'
        else:
            mbAddrN = "not available"
        
        xW = -1
        yW = -1
        if mbAddrN == 'not available':
            return None
        else:
            xW = (xN+maxW)%maxW
            yW = (yN+maxH)%maxH
            idx = luma_block_indices_4x4(xW, yW)
            return idx
        
        return None

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

#6.4.11.4

#6.4.13.1
def luma_block_indices_4x4(xP, yP):
    idx = 8 * ( yP // 8 ) + 4 * ( xP // 8 ) + 2 * ( ( yP % 8 ) // 4 ) + ( ( xP % 8 ) // 4 )
    return idx

for i in range(16):
    print(inverse_4x4_luma_block_scanning_process(i))