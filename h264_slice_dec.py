import numpy as py
import h264_slice_data
from h264_mb import Macroblock
import numpy as np
import cal
import math
import h264scan

def dec(sl :h264_slice_data.H264SliceData):
    if sl.header.slice_type == "I":
        dec_intra(sl)
    else:
        raise Exception("NOT IMP")


def dec_intra(sl :h264_slice_data.H264SliceData):
    for mb in sl.mbs:
        dec_intra_mb(sl, mb)

def dec_intra_mb(sl :h264_slice_data.H264SliceData, mb:Macroblock):

    #8.3
    dcPredModePredictedFlag = 0
    mba:Macroblock = None 
    mbb:Macroblock = None 

    if mb.mbAddrA != None:
        mba = sl.mbs[mb.mbAddrA]
    if mb.mbAddrA != None:
        mbb = sl.mbs[mb.mbAddrB]

    if mb.mbAddrA == None or mb.mbAddrB == None:
        dcPredModePredictedFlag = 1
    if (mb.mbAddrA != None and (not 'Intra' in mba.MbPartPredMode)) and sl.pps.constrained_intra_pred_flag == 1:
        dcPredModePredictedFlag = 1
    if (mb.mbAddrB != None and (not 'Intra' in mbb.MbPartPredMode)) and sl.pps.constrained_intra_pred_flag == 1:
        dcPredModePredictedFlag = 1
    
    intraMxMPredModeA = 2
    intraMxMPredModeB = 2
    for i in range(16):
        if dcPredModePredictedFlag == 0 and (mba.MbPartPredMode in ['Intra_4x4', 'Intra_8x8']):
            if mba.MbPartPredMode == "Intra_4x4":
                intraMxMPredModeA = mba.Intra4x4PredMode[i]
                intraMxMPredModeB = mbb.Intra4x4PredMode[i]
            else:
                intraMxMPredModeA = mba.Intra4x4PredMode[i>>2]
                intraMxMPredModeB = mbb.Intra4x4PredMode[i>>2]

        preIntra4x4PreMode = min(intraMxMPredModeA, intraMxMPredModeB)
        if mb.prev_intra4x4_pred_mode_flag[i]:
            mb.Intra4x4PredMode[i] = preIntra4x4PreMode
        else:
            if mb.rem_intra4x4_pred_mode[i] < preIntra4x4PreMode:
                mb.Intra4x4PredMode[i] = mb.rem_intra4x4_pred_mode[i]
            else:
                mb.Intra4x4PredMode[i] = mb.rem_intra4x4_pred_mode[i] + 1
    
    #8.5.1
    if mb.transform_size_8x8_flag == 0:
        inverse_scanning_4x4_transform_coeff(mb)
    
    r = mb.C_l
    if mb.TransformBypassModeFlag != 1:
        d = scaling_and_transformation_4x4_luma(mb)
        r = tranformation_residual_4x4_blocks(d)

    if mb.TransformBypassModeFlag == 1 and mb.MbPartPredMode == 'Intra_4x4' :
        for blkidx in range(16):
            if mb.Intra4x4PredMode[blkidx] == 0 or mb.Intra4x4PredMode[blkidx] == 1:
                r[blkidx]  = intra_residual_tranform_bypass_decoding(4, 4, mb.Intra4x4PredMode[blkidx], r[blkidx])
    
    xO, yO = h264scan.inverse_4x4_luma_block_scanning_process()



ZIG_ZAG_4x4_MAP = [
    [0, 0],[0,1], [1,0], [2,0], [1, 1], [0, 2], [0, 3], [1, 2], [2, 1], [3, 0], [ 3, 1], [2, 2], [1, 3], [2, 3], [3, 2], [3, 3]
]

def inverse_scanning_4x4_transform_coeff(mb: Macroblock):
    for blkidx in range(16):
        for i in range(16):
            x, y  = ZIG_ZAG_4x4_MAP[i][0], ZIG_ZAG_4x4_MAP[i][1]
            mb.C_l[blkidx][x][y] = mb.LumaLevel4x4[blkidx][i]

def scaling_and_transformation_4x4_luma(mb :Macroblock):
    bitDepth = mb.sps.BitDepthY
    qP = mb.QP_1_y

    sMbFlag = 0
    if mb.slice_type == "SI" or (mb.slice_type == "SP" and (not 'Intra' in mb.MbPartPredMode)):
        sMbFlag = 1
    if sMbFlag == 1:
        raise Exception("NOT IMP")
    
    d = np.zeros(shape=(16, 4, 4), dtype=np.int32)
    if mb.MbPartPredMode == 'Intra_16x16':
        for blkidx in range(16):
            d[blkidx][0][0] = mb.C_l[blkidx][0][0]
    
    for blkidx in range(16):
        for i in range(4):
            for j in range(4):
                if qP >= 24:
                    d[blkidx][i][j] = (mb.C_l[blkidx][i][j] * cal.LevelScale4x4(qP%6, i, j)) << (qP//6-4)
                else:
                    d[blkidx][i][j] = (mb.C_l[blkidx][i][j] * cal.LevelScale4x4(qP%6, i, j) + 2**(3-qP/6)) >> (4 - qP//6)
    
    return d

def tranformation_residual_4x4_blocks(d:np.array):
    e = np.zeros(shape=(4,4), dtype=np.int32)
    f = np.zeros(shape=(4,4), dtype=np.int32)
    g = np.zeros(shape=(4,4), dtype=np.int32)
    h = np.zeros(shape=(4,4), dtype=np.int32)
    r = np.zeros(shape=(4,4), dtype=np.int32)
    for i in range(4):
        e[i][0] = d[i][0] + d[i][2]
        e[i][1] = d[i][0] - d[i][2]
        e[i][2] = (d[i][1] >> 1) - d[i][3]
        e[i][3] = d[i][1] + (d[i][3] >> 1)
    
    for i in range(4):
        f[i][0] = e[i][0] + e[i][3]
        f[i][1] = e[i][1] + e[i][2]
        f[i][2] = e[i][1] - e[i][2]
        f[i][3] = e[i][0] - e[i][3]
    
    for j in range(4):
        g[0][j] = f[0][j] + f[2][j]
        g[1][j] = f[0][j] - f[2][j]
        g[2][j] = (f[1][j]>>1) - f[3][j]
        g[3][j] = f[1][j] + (f[3][j] >> 1)
    
    for h in range(4):
        h[0][j] = g[0][j] + g[3][j]
        h[1][j] = g[1][j] + g[2][j]
        h[2][j] = g[2][j] - g[2][j]
        h[3][j] = g[0][j] - g[3][j]
    
    for i in range(4):
        for j in range(4):
            r[i][j] = (h[i][j] + 2 ** 5) >> 6
    
    return r

def intra_residual_tranform_bypass_decoding(nW, nH, horPredFlag, r :np.array):
    f = np.zeros(shape=(nW, nH), dtype=np.int32)

    for i in range(nH):
        for j in range(nW):
            f[i][j] = r[i][j]
    
    if horPredFlag == 0:
        for i in range (nH):
            for j in range (nW):
                tmp = 0
                for k in range(i+1):
                    tmp += f[k][j]
                r[i][j] = tmp
    else:
        for i in range(nH):
            for j in range(nW):
                tmp = 0
                for k in range(j+1):
                    tmp += f[i][k]
                r[i][j] = tmp
    return f

