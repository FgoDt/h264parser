from rbsp import RBSPBits
from h264_cavlc import H264CAVLCDec
from h264_cabac_dec import H264CABACDec
import h264pps
import h264sps
import numpy as np
import h264scan

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
 ['P_L0_16x16'    ,1  ,'Pred_L0' ,'na'        ,16 ,16]
,['P_L0_L0_16x8'  ,2  ,'Pred_L0' ,'Pred_L0'   ,16 ,8]
,['P_L0_L0_8x16'  ,2  ,'Pred_L0' ,'Pred_L0'   ,8  ,16]
,['P_8x8'         ,4  ,'na'      ,'na'        ,8  ,8]
,['P_8x8ref0'     ,4  ,'na'      ,'na'        ,8  ,8]
,['P_Skip'        ,1  ,'Pred_L0' ,'na'        ,16 ,16]
]

SI_SLICE_TYPE = ['SI', 'Intra_4x4', 'na', 'na', 'na']

I_SLICE_TYPE = [
 ['I_NxN',         0    ,'Intra_4x4'   ,'na' ,'na' ,'na'] 
,['I_NxN',         1    ,'Intra_8x8'   ,'na' ,'na' ,'na']
,['I_16x16_0_0_0', 'na'  ,'Intra_16x16', 0    ,0    ,0]
,['I_16x16_1_0_0', 'na'  ,'Intra_16x16', 1    ,0    ,0]
,['I_16x16_2_0_0', 'na'  ,'Intra_16x16', 2    ,0    ,0]
,['I_16x16_3_0_0', 'na'  ,'Intra_16x16', 3    ,0    ,0]
,['I_16x16_0_1_0', 'na'  ,'Intra_16x16', 0    ,1    ,0]
,['I_16x16_1_1_0', 'na'  ,'Intra_16x16', 1    ,1    ,0]
,['I_16x16_2_1_0', 'na'  ,'Intra_16x16', 2    ,1    ,0]
,['I_16x16_3_1_0', 'na'  ,'Intra_16x16', 3    ,1    ,0]
,['I_16x16_0_2_0', 'na'  ,'Intra_16x16', 0    ,2    ,0]
,['I_16x16_1_2_0', 'na'  ,'Intra_16x16', 1    ,2    ,0]
,['I_16x16_2_2_0', 'na'  ,'Intra_16x16', 2    ,2    ,0]
,['I_16x16_3_2_0', 'na'  ,'Intra_16x16', 3    ,2    ,0]
,['I_16x16_0_0_1', 'na'  ,'Intra_16x16', 0    ,0    ,15]
,['I_16x16_1_0_1', 'na'  ,'Intra_16x16', 1    ,0    ,15]
,['I_16x16_2_0_1', 'na'  ,'Intra_16x16', 2    ,0    ,15]
,['I_16x16_3_0_1', 'na'  ,'Intra_16x16', 3    ,0    ,15]
,['I_16x16_0_1_1', 'na'  ,'Intra_16x16', 0    ,1    ,15]
,['I_16x16_1_1_1', 'na'  ,'Intra_16x16', 1    ,1    ,15]
,['I_16x16_2_1_1', 'na'  ,'Intra_16x16', 2    ,1    ,15]
,['I_16x16_3_1_1', 'na'  ,'Intra_16x16', 3    ,1    ,15]
,['I_16x16_0_2_1', 'na'  ,'Intra_16x16', 0    ,2    ,15]
,['I_16x16_1_2_1', 'na'  ,'Intra_16x16', 1    ,2    ,15]
,['I_16x16_2_2_1', 'na'  ,'Intra_16x16', 2    ,2    ,15]
,['I_16x16_3_2_1', 'na'  ,'Intra_16x16', 3    ,2    ,15]
,['I_PCM'        , 'na'  ,'na'         , 'na' ,'na' ,'na']
]

def GetxDyD(N, mb_type='-', currSubMbType='-'):
    if N == "A":
        return (-1, 0)
    if N == "B":
        return (0, -1)
    if N == "C":
        prePartWidth = 0
        if mb_type in ['P_Skip', 'B_Direct_16x16']:
            prePartWidth = 16
        elif mb_type == 'B_8x8':
            if currSubMbType == "B_Direct_8x8":
                prePartWidth = 16
            else:
                prePartWidth = SubMbPartWidth()
        elif mb_type in ['P_8x8', 'P_8x8ref0']:
            prePartWidth = SubMbPartWidth()
        else:
            prePartWidth = MbPartWidth(mb_type)
        return (prePartWidth, -1)
    if N == "D":
        return (-1, -1)

def GetMbTypeMap(mb_type, slice_type, transform_8x8_mode_flag=0):
    if slice_type == 'I':
        if transform_8x8_mode_flag == 1 or mb_type > 0:
            mb_type += 1
        return I_SLICE_TYPE[mb_type]
    if slice_type == 'SI':
        if mb_type == 0:
            return SI_SLICE_TYPE[mb_type]
        else:
            return I_SLICE_TYPE[mb_type - 1]
    if slice_type == 'P' or slice_type == 'SP':
        if mb_type < 5:
            return P_SP_SLICE_TYPE[MbTypeName]
        else:
            return I_SLICE_TYPE[mb_type - 5]
    if slice_type == 'B':
        if mb_type < 23:
            return B_SLICES_MB_TYPE[mb_type]
        else:
            return I_SLICES_MB_TYPE[mb_type - 23]

def MbTypeName(mb_type, slice_type, transform_8x8_mode_flag=0):
    return GetMbTypeMap(mb_type, slice_type, transform_8x8_mode_flag)[0]


def MbPartPredMod(mb_type, slice_type, transform_8x8_mode_flag, param=0):
    slice_map = GetMbTypeMap(mb_type, slice_type, transform_8x8_mode_flag)
    idx = 2
    if slice_type == "SI":
        idx = 1
    if param == 1:
        if slice_type == 'I' or slice_type == 'SI':
            raise Exception("slice type error, this slice no MbpartPredMode(mb_type, 1) define")
        idx = 3
    return slice_map[idx]

def NumMbPart(mb_type, slice_type, transform_8x8_mode_flag):
    return GetMbTypeMap(mb_type, slice_type, transform_8x8_mode_flag)[1]

def CodedBlockPatternLuma(mb_type, slice_type, transform_8x8_mode_flag, coded_block_pattern):
    if slice_type != 'I' and slice_type != 'SI':
        raise Exception("slice type error, this slice no CodedBlockPatternLuma")
    if mb_type == 0:
        return coded_block_pattern % 16
    slice_map = GetMbTypeMap(mb_type, slice_type, transform_8x8_mode_flag)
    return slice_map[5]

def CodedBlockPatternChroma(mb_type, slice_type, transform_8x8_mode_flag, coded_block_pattern):
    if slice_type != 'I' and slice_type != 'SI':
        raise Exception("slice type error, this slice no CodedBlockPatternLuma")
    if mb_type == 0:
        return coded_block_pattern / 16
    slice_map = GetMbTypeMap(mb_type, slice_type, transform_8x8_mode_flag)
    return slice_map[4]

def ChromaArrayType(sps):
    return 0 if sps['separate_colour_plane_flag'] == 1 else sps['chroma_format_idc']

class Macroblock:
    def __init__(self, slice_header, sps, pps, rbsp:RBSPBits):
        self.rbsp = rbsp
        self.sheader =  slice_header
        self.sps = sps
        self.pps = pps
        self.cavlc = None
        self.cabac = None
        self.slice_type = slice_header['slice_type']
        self.transform_8x8_mode_flag = pps['transform_8x8_mode_flag']
        self.transform_size_8x8_flag = 0
        pass


    def dec(self):
        if not self.pps['entropy_coding_mode_flag']:
            self.cavlc = H264CAVLCDec(self.rbsp)
            self.raw_mb_type = self.rbsp.ue()
        else:
            self.cabac = H264CABACDec(self.sheader, self.sps, self.pps, self.rbsp)
            self.raw_mb_type = ae()

        self.mb_type = MbTypeName(self.raw_mb_type, self.slice_type, self.transform_8x8_mode_flag)


        if self.mb_type == 'I_PCM':
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
            self.MbPartPredMode = MbPartPredMod(self.raw_mb_type, self.slice_type, self.transform_8x8_mode_flag)

            if self.mb_type != 'I_NxN' and self.MbPartPredMode != 'Intra_16x16' and NumMbPart(self.mb_type, self.slice_type, self.transform_8x8_mode_flag) == 4:
                self.sub_mb = []
                sub_mb_pred(self.mb_type)
                for mbPartIdx in range(4):
                    if self.sub_mb[mbPartIdx].type != 'B_Direct_8x8':
                        if NumSubMbPart(self.sub_mb[mbPartIdx].type) > 1:
                            noSubMbPartSizeLessThan8x8Flag = 0
                    elif not self.sps['direct_8x8_inference_flag']:
                        noSubMbPartSizeLessThan8x8Flag = 0
            else:
                if self.transform_8x8_mode_flag and self.mb_type == 'I_NxN':
                    if self.cavlc != None:
                        self.transform_size_8x8_flag = self.cavlc.rbsp.u(1)
                    else:
                        self.transform_size_8x8_flag = self.cabac.ae()
                self.mb_pred()
            
            if self.MbPartPredMode != 'Intra_16x16':
                if self.cavlc != None:
                    self.coded_block_pattern = self.rbsp.me(ChromaArrayType(self.sps))
                else:
                    self.coded_block_pattern = self.cabac.ae()
                
                if ((CodedBlockPatternLuma(self.raw_mb_type, self.slice_type, self.transform_8x8_mode_flag, self.coded_block_pattern) > 0) and 
                    (self.transform_8x8_mode_flag == 1) and (self.mb_type != 'I_NxN') and (noSubMbPartSizeLessThan8x8Flag == 1) and
                    (self.mb_type != 'B_Direct_16x16' or self.sps['direct_8x8_inference_flag'])):
                    if self.cavlc != None:
                        self.transform_size_8x8_flag = self.cavlc.rbsp.u(1)
                    else:
                        self.transform_size_8x8_flag = self.cabac.ae()
                if ((CodedBlockPatternLuma(self.raw_mb_type, self.slice_type, self.transform_8x8_mode_flag, self.coded_block_pattern) > 0) or 
                    (CodedBlockPatternChroma(self.raw_mb_type, self.slice_type, self.transform_8x8_mode_flag, self.coded_block_pattern) > 0) or 
                    (self.MbPartPredMode == 'Intra_16x16')):
                    if self.cavlc != None:
                        self.mb_qp_delta = self.cavlc.rbsp.se()
                    else:
                        self.mb_qp_delta = self.cabac.ae()
                    self.residual(0, 15)

    def mb_pred(self):
        if self.MbPartPredMode in ['Intra_4x4', 'Intra_8x8', 'Intra_16x16']:
            if self.MbPartPredMode == 'Intra_4x4':
                self.prev_intra4x4_pred_mode_flag = []
                self.rem_intra4x4_pred_mode = []
                for luma4x4BlkIdx in range(16):
                    flag = 0
                    if self.cavlc != None:
                        flag = self.rbsp.u(1)
                    else:
                        flag = self.cabac.ae()
                    self.prev_intra4x4_pred_mode_flag.append(flag)
                    if not flag :
                        mode = 0
                        if self.cavlc != None:
                            mode = self.rbsp.u(3)
                        else:
                            mode = self.cabac.ae()
                        self.rem_intra4x4_pred_mode.append(mode)

            if self.MbPartPredMode == 'Intra_8x8':
                self.prev_intra8x8_pred_mode_flag = []
                self.rem_intra8x8_pred_mode = []
                for luma4x4BlkIdx in range(16):
                    flag = 0
                    if self.cavlc != None:
                        flag = self.rbsp.u(1)
                    else:
                        flag = self.cabac.ae()
                    self.prev_intra8x8_pred_mode_flag.append(flag)
                    if not flag :
                        mode = 0
                        if self.cavlc != None:
                            mode = self.rbsp.u(3)
                        else:
                            mode = self.cabac.ae()
                        self.rem_intra8x8_pred_mode.append(mode)
            if ChromaArrayType(self.sps) == 1 or ChromaArrayType(self.sps) == 2:
                if self.cavlc != None:
                    self.intra_chroma_pred_mode = self.rbsp.ue()
                else:
                    self.intra_chroma_pred_mode = self.cabac.ae()
        elif self.MbPartPredMode != 'Direct':
            self.numMbPart = NumMbPart(self.raw_mb_type, self.slice_type, self.transform_8x8_mode_flag)
            for mbPartIdx in range(self.numMbPart):
                if ((self.pps['num_ref_idx_10_active_minus1'] > 0 or self.header['mb_field_decoding_flag'] != self.header['field_pic_flag']) and  
                    MbPartPredMod(self.mb_type, self.slice_type, self.transform_8x8_mode_flag, mbPartIdx) != 'Pred_L1'):
                    self.ref_idx_10[mbPartIdx] = self.cavlc.te()
            for mbPartIdx in range(self.numMbPart):
                if ((self.pps['num_ref_idx_10_active_minus1'] > 0 or self.header['mb_field_decoding_flag'] != self.header['field_pic_flag']) and  
                    MbPartPredMod(self.mb_type, self.slice_type, self.transform_8x8_mode_flag, mbPartIdx) != 'Pred_L1'):
                    self.ref_idx_11[mbPartIdx] = self.cavlc.te()
            for mbPartIdx in range(self.numMbPart):
                if MbPartPredMod(self.mb_type, self.slice_type, self.transform_8x8_mode_flag, mbPartIdx) != 'Pred_L1':
                    for compIdx in range(2):
                        assert False
            for mbPartIdx in range(self.numMbPart):
                if MbPartPredMod(self.mb_type, self.slice_type, self.transform_8x8_mode_flag, mbPartIdx) != 'Pred_L0':
                    for compIdx in range(2):
                        assert False

    def residual(self, startIdx, endIdx):
        if self.cavlc != None:
            self.residual_block = self.residual_block_cavlc
        else:
            self.residual_block = None
        
        self.i16x16DClevel = np.array(16)
        self.i16x16AClevel = np.array(15)
        self.level4x4 = np.zeros(shape=(16,16), dtype=np.int32)
        self.level8x8 = []
        self.startIdx = startIdx
        self.endIdx = endIdx

        self.residual_luma(self.i16x16DClevel, self.i16x16AClevel, self.level4x4, self.level8x8, self.startIdx, self.endIdx)

    def residual_luma(self, i16x16DClevel, i16x16AClevel, level4x4, level8x8, startIdx, endIdx):
        self.coded_block_pattern_luma = CodedBlockPatternLuma(self.raw_mb_type, self.slice_type, self.transform_8x8_mode_flag, self.coded_block_pattern)
        if startIdx == 0 and self.MbPartPredMode == 'Intra_16x16':
            self.residual_block(i16x16DClevel, 0, 15, 16)
        for i8x8 in range(4):
            if (not self.transform_size_8x8_flag) or self.cavlc != None:
                for i4x4 in range(4):
                    if self.coded_block_pattern_luma & (1 << i8x8):
                        if self.MbPartPredMode == 'Intra_16x16':
                            self.residual_block(i16x16AClevel[i8x8*4+i4x4], max(0, startIdx -1), endIdx-1, 15)
                        else:
                            luma4x4BlkIdx = i8x8 * 4 + i4x4
                            xDyD = GetxDyD('A', self.mb_type)
                            blkA = h264scan.derivation_process_neighbouring_4x4_luma_blocks(luma4x4BlkIdx,xDyD[0], xDyD[1])
                            #xDyD = GetxDyD('B', self.mb_type)
                            #blkB = h264scan.derivation_process_neighbouring_4x4_luma_blocks(luma4x4BlkIdx,xDyD[0], xDyD[1])
                            nC = 0
                            coeff_token, vals = self.cavlc.ce_coeff_token(nC)
                            self.coeff_token = coeff_token
                            self.TrailingOnes = vals[0]
                            self.TotalCoeff = vals[1]
                            

                            self.residual_block(level4x4[i8x8*4+i4x4], startIdx, endIdx, 16)
                    elif self.MbPartPredMode == 'Intra_16x16':
                        for i in range(15):
                            i16x16AClevel[i8x8*4 + i4x4][i] = 0
                    else:
                        for i in range(16):
                            level4x4[i8x8 * 4 + i4x4][i] = 0
                    if self.cavlc != None and self.transform_size_8x8_flag:
                        for i in range(16):
                            level8x8[i8x8][4*i+i4x4] = level4x4[i8x8*4 + i4x4][i]
            elif self.coded_block_pattern_luma & (1 << i8x8):
                self.residual_block(level8x8[i8x8], 4 * startIdx, 4 * endIdx + 3, 64)
            else:
                for i in range(64):
                    level8x8[i8x8][i] = 0
        print(level4x4)
    
    def residual_block_cavlc(self, coeffLevel, startIdx, endIdx, maxNumCoeff):
        for i in range (maxNumCoeff):
            coeffLevel[i] = 0
        
        if self.TotalCoeff > 0 :
            if self.TotalCoeff > 10 and self.TrailingOnes < 3:
                suffixLength = 1
            else:
                suffixLength = 0
            levelVal = np.zeros(shape=(self.TotalCoeff), dtype=np.int32)
            for i in range(self.TotalCoeff):
                if i < self.TrailingOnes:
                    trailing_ones_sign_flag = self.rbsp.u(1)
                    levelVal[i] = 1 - 2 * trailing_ones_sign_flag
                else:
                    level_prefix = self.cavlc.ce_level_prefix()
                    levelCode = (min(15, level_prefix) << suffixLength)
                    levelSuffixSize = suffixLength
                    if level_prefix == 14 and suffixLength == 0:
                        levelSuffixSize = 4
                    elif level_prefix == 15:
                        levelSuffixSize = level_prefix - 3

                    if suffixLength > 0 or level_prefix >= 14:
                        level_suffix = 0
                        if levelSuffixSize > 0:
                            level_suffix = self.rbsp.u(levelSuffixSize)
                        levelCode += level_suffix
                    
                    if level_prefix >= 15 and suffixLength == 0:
                        levelCode += 15
                    if level_prefix >= 16:
                        levelCode += (1 << (level_prefix - 3)) - 4096
                    if i == self.TrailingOnes and self.TrailingOnes < 3:
                        levelCode += 2
                    if levelCode % 2 == 0:
                        levelVal[i] = (levelCode+2) >> 1
                    else:
                        levelVal[i] = (-levelCode -1) >> 1
                    if suffixLength == 0:
                        suffixLength = 1
                    if abs(levelVal[i]) > ( 3 << (suffixLength - 1)) and suffixLength < 6:
                        suffixLength += 1
            
            zerosLeft = 0
            if self.TotalCoeff < endIdx - startIdx + 1:
                tzVlcIndex = self.TotalCoeff
                key, total_zeros = self.cavlc.ce_total_zeros(tzVlcIndex)
                zerosLeft = total_zeros

            runVal = np.zeros(shape=(self.TotalCoeff), dtype=np.int32)
            for i in range (self.TotalCoeff):
                if zerosLeft > 0 :
                    key, run_before = self.cavlc.ce_run_before(zerosLeft)
                    runVal[i] = run_before
                else:
                    runVal[i] = 0
                zerosLeft = zerosLeft - runVal[i]
            runVal[self.TotalCoeff - 1] = zerosLeft
            coeffNum = -1
            for i in range(self.TotalCoeff):
                coeffNum += runVal[i] + 1
                coeffLevel[startIdx + coeffNum] = levelVal[i]
            
        print("done residual block cavlc")
        pass

    def residual_block_cabac(self, coeffLevel, startIdx, endIdx, maxNumCoeff):
        pass