from rbsp import RBSPBits
from h264_cavlc_dec import H264CAVLCDec
from h264_cabac_dec import H264CABACDec
import h264pps
import h264sps

I_SLICES_MB_TYPE_NAME = ['I_NxN','I_17x16_0_0_0', 'I_16x16_1_0_0', 'I_16x16_2_0_0', 'I_16x16_3_0_0', 
                        'I_16x16_0_1_0', 'I_16x16_1_1_0', 'I_16x16_2_1_0', 'I_16x16_3_1_0', 'I_16x16_0_2_0', 
                        'I_16x16_1_2_0', 'I_16x16_2_2_0', 'I_16x16_3_2_0', 'I_16x16_0_0_1', 'I_16x16_1_0_1', 
                        'I_16x16_2_0_1', 'I_16x16_3_0_1', 'I_16x16_0_1_1', 'I_16x16_1_1_1', 'I_16x16_2_1_1', 
                        'I_16x16_3_1_1', 'I_16x16_0_2_1', 'I_16x16_1_2_1', 'I_16x16_2_2_1', 'I_16x16_3_2_1', 
                        'I_PCM']
P_SP_SLICES_MB_TYPE_NAME = ['P_L0_16x16', 'P_L0_L0_16x8', 'P_L0_L0_8x16', 'P_8x8', 'P_8x8ref0', 'P_Skip' ]

SI_SLICES_MB_TYPE_NAME = ['SI']

B_SLICES_MB_TYPE_NAME = ['B_Direct_16x16', 'B_L0_16x16', 'B_L1_16x16', 'B_Bi_16x16', 'B_L0_L0_16x8', 
                        'B_L0_L0_8x16', 'B_L1_L1_16x8', 'B_L1_L1_8x16', 'B_L0_L1_16x8', 'B_L0_L1_8x16',
                        'B_L1_L0_16x8', 'B_L1_L0_8x16', 'B_L0_Bi_16x8', 'B_L0_Bi_8x16', 'B_L1_Bi_16x8',
                        'B_L1_Bi_8x16', 'B_Bi_L0_16x8', 'B_Bi_L0_8x16', 'B_Bi_L1_16x8', 'B_Bi_L1_8x16', 
                        'B_Bi_Bi_16x8', 'B_Bi_Bi_8x16', 'B_8x8', 'B_Skip']

B_SLICES_MB_TYPE=[
 ['B_Direct_16x16' ,'na'   ,'Direct'   ,'na'       ,8  ,8]
,['B_L0_16x16'    ,1      ,'Pred_L0'  ,'na'       ,16 ,16]
,['B_L1_16x16'    ,1      ,'Pred_L1'  ,'na'       ,16 ,16]
,['B_Bi_16x16'    ,1      ,'BiPred'   ,'na'       ,16 ,16]
,['B_L0_L0_16x8'  ,2      ,'Pred_L0'  ,'Pred_L0'  ,16 ,8]
,['B_L0_L0_8x16'  ,2      ,'Pred_L0'  ,'Pred_L0'  ,8  ,16]
,['B_L1_L1_16x8'  ,2      ,'Pred_L1'  ,'Pred_L1'  ,16 ,8]
,['B_L1_L1_8x16'  ,2      ,'Pred_L1'  ,'Pred_L1'  ,8  ,16]
,['B_L0_L1_16x8'  ,2      ,'Pred_L0'  ,'Pred_L1'  ,16 ,8]
,['B_L0_L1_8x16'  ,2      ,'Pred_L0'  ,'Pred_L1'  ,8  ,16]
,['B_L1_L0_16x8'  ,2      ,'Pred_L1'  ,'Pred_L0'  ,16 ,8]
,['B_L1_L0_8x16'  ,2      ,'Pred_L1'  ,'Pred_L0'  ,8  ,16]
,['B_L0_Bi_16x8'  ,2      ,'Pred_L0'  ,'BiPred'   ,16 ,8]
,['B_L0_Bi_8x16'  ,2      ,'Pred_L0'  ,'BiPred'   ,8  ,16]
,['B_L1_Bi_16x8'  ,2      ,'Pred_L1'  ,'BiPred'   ,16 ,8]
,['B_L1_Bi_8x16'  ,2      ,'Pred_L1'  ,'BiPred'   ,8  ,16]
,['B_Bi_L0_16x8'  ,2      ,'BiPred'   ,'Pred_L0'  ,16 ,8]
,['B_Bi_L0_8x16'  ,2      ,'BiPred'   ,'Pred_L0'  ,8  ,16]
,['B_Bi_L1_16x8'  ,2      ,'BiPred'   ,'Pred_L1'  ,16 ,8]
,['B_Bi_L1_8x16'  ,2      ,'BiPred'   ,'Pred_L1'  ,8  ,16]
,['B_Bi_Bi_16x8'  ,2      ,'BiPred'   ,'BiPred'   ,16 ,8]
,['B_Bi_Bi_8x16'  ,2      ,'BiPred'   ,'BiPred'   ,8  ,16]
,['B_8x8'         ,4      ,'na'       ,'na'       ,8  ,8]
,['B_Skip'        ,'na'   ,'Direct'   ,'na'       ,8  ,8]]

P_SP_SLICE_TYPE = [
'P_L0_16x16'    ,1  ,'Pred_L0' ,'na'        ,16 ,16
,'P_L0_L0_16x8'  ,2  ,'Pred_L0' ,'Pred_L0'   ,16 ,8
,'P_L0_L0_8x16'  ,2  ,'Pred_L0' ,'Pred_L0'   ,8  ,16
,'P_8x8'         ,4  ,'na'      ,'na'        ,8  ,8
,'P_8x8ref0'     ,4  ,'na'      ,'na'        ,8  ,8
,'P_Skip'        ,1  ,'Pred_L0' ,'na'        ,16 ,16
]

def MbTypeName(mb_type, slice_type):
    if slice_type == 'I':
        return I_SLICES_MB_TYPE_NAME[mb_type]
    if slice_type == 'SI':
        if mb_type == 0:
            return SI_SLICES_MB_TYPE_NAME[mb_type]
        else:
            return I_SLICES_MB_TYPE_NAME[mb_type - 1]
    if slice_type == 'P' or slice_type == 'SP':
        if mb_type < 5:
            return P_SP_SLICES_MB_TYPE_NAME[MbTypeName]
        else:
            return I_SLICES_MB_TYPE_NAME[mb_type - 5]
    if slice_type == 'B':
        if mb_type < 23:
            return B_SLICES_MB_TYPE_NAME[mb_type]
        else:
            return I_SLICES_MB_TYPE_NAME[mb_type - 23]

def I_MbpartPredMod(mb_type, transform_8x8_mode_flag):
    if mb_type == 0 :
        if transform_8x8_mode_flag == 1:
            return 'Intra_8x8'
        else:
            return 'Intra_4x4'
    elif mb_type < 25:
        return 'Intra_16x16'
    else:
        return 'na'

def MbPartPredMod(mb_type, slice_type, transform_8x8_mode_flag):
    if slice_type == 'I':
        return I_MbpartPredMod(mb_type, transform_8x8_mode_flag)
    if slice_type == 'SI':
        if mb_type == 0:
            return 'Intra_4x4'
        else:
            return I_MbpartPredMod(mb_type, transform_8x8_mode_flag)
    if slice_type == 'P' or slice_type == 'SP':
        if mb_type == 0:
            return 


def GetMbType(slice_type, mb_type, transform_8x8_mode_flag, coded_block_pattern):
    idx = mb_type + 1
    if mb_type == 0 and transform_8x8_mode_flag == 0 :
        idx = 0
    ret = I_SLICES_MB_TYPE[idx]
    if mb_type == 0:
        chroma = coded_block_pattern//16
        luma = coded_block_pattern%16
        ret[3] = chroma
        ret[4] = luma
    return ret


class Macroblock:
    def __init__(self, slice_header, sps, pps, rbsp:RBSPBits):
        self.rbsp = rbsp
        self.sheader =  slice_header
        self.sps = sps
        self.pps = pps
        self.cavlc = None
        self.cabac = None
        pass

    def dec(self):
        if not self.pps['entropy_coding_mode_flag']:
            self.cavlc = H264CAVLCDec(self.sps, self.pps, self.sheader, self.rbsp)
            self.mb_type = self.rbsp.ue()
        else:
            self.cabac = H264CABACDec(self.sheader, self.sps, self.pps, self.rbsp)
            self.mb_type = ae()
        if self.mb_type == I_PCM:
            self.rbsp.byte_aligned()
            self.pcm_alignment_zero_bit = self.rbsp.f(1)
            self.pcm_sample_luma = []
            self.pcm_sample_chroma = []
            for i in range (256):
                v = h264sps.BitDepthY(self.sps)
                self.pcm_sample_luma.append(self.rbsp.u(v))
            for i in range ( 2 * h264sps.MbWidthC(self.sps) * h264sps.MbHeightC(self.sps)):
                v = h264sps.BitDepthC(self.sps)
                self.pcm_sample_chroma.append(self.rbsp.u(v))
        else:
            noSubMbPartSizeLessThan8x8Flag = 1
            if self.mb_type != I_NxN and MbPartPredMode(self.mb_type, 0) != Intra_16x16 and NumMbPart(self.mb_type) == 4:
                sub_mb_pred(self.mb_type)

        


def MbPartPredMode(type, n):
    pass