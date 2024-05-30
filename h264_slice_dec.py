import numpy as py
import h264_slice_data
from h264_mb import Macroblock
import numpy as np
import cal
import math

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
    
    if mb.TransformBypassModeFlag != 1:
        scaling_and_transformation_4x4_luma(mb)


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
