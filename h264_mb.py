from rbsp import RBSPBits
from h264_cavlc import H264CAVLCDec
from h264_cabac_dec import H264CABACDec
from h264_slice_data import H264SliceData
import h264_pps
import h264_sps
import h264_slice_header
import h264scan
import numpy as np

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
 [['I_NxN',         0    ,'Intra_4x4'   ,'na' ,'na' ,'na'] ,['I_NxN',         1    ,'Intra_8x8'   ,'na' ,'na' ,'na']]
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

SUB_MB_P_TYPE=[
 ['inferred', 'na', 'na', 'na', 'na',]
,['P_L0_8x8', 1, 'Pred_L0', 8, 8,]
,['P_L0_8x4', 2, 'Pred_L0', 8, 4,]
,['P_L0_4x8', 2, 'Pred_L0', 4, 8,]
,['P_L0_4x4', 4, 'Pred_L0', 4, 4,]
]

SUB_MB_B_TYPE = [
['inferred' 'mb_type'        ,4 ,'Direct'   ,4 ,4],
[0,         'B_Direct_8x8'   ,4 ,'Direct'   ,4 ,4],
[1,         'B_L0_8x8'       ,1 ,'Pred_L0'  ,8 ,8],
[2,         'B_L1_8x8'       ,1 ,'Pred_L1'  ,8 ,8],
[3,         'B_Bi_8x8'       ,1 ,'BiPred'   ,8 ,8],
[4,         'B_L0_8x4'       ,2 ,'Pred_L0'  ,8 ,4],
[5,         'B_L0_4x8'       ,2 ,'Pred_L0'  ,4 ,8],
[6,         'B_L1_8x4'       ,2 ,'Pred_L1'  ,8 ,4],
[7,         'B_L1_4x8'       ,2 ,'Pred_L1'  ,4 ,8],
[8,         'B_Bi_8x4'       ,2 ,'BiPred'   ,8 ,4],
[9,         'B_Bi_4x8'       ,2 ,'BiPred'   ,4 ,8],
[10,        'B_L0_4x4'       ,4 ,'Pred_L0'  ,4 ,4],
[11,        'B_L1_4x4'       ,4 ,'Pred_L1'  ,4 ,4],
[12,        'B_Bi_4x4'       ,4 ,'BiPred'   ,4 ,4],
]



class block:
    def __init__(self, TotalCoeff):
        self.TotalCoeff = TotalCoeff
        self.type = None
        self.level = None
        pass

class SubMb:
    def __init__(self, raw_mb_type, mb_type):
        self.raw_mb_type = raw_mb_type
        self.mb_type = mb_type
        self.cal_default()
        self.ref_idx_l0 = None
        self.ref_idx_l1 = None
        pass

    def cal_default(self):
        self.type_name = None
        if self.mb_type == "P":
            self.type_name = SUB_MB_P_TYPE[self.raw_mb_type+1][0]
            self.NumSubMbPart = SUB_MB_P_TYPE[self.raw_mb_type+1][1]
            self.SubMbPredMode = SUB_MB_P_TYPE[self.raw_mb_type+1][2]
            self.SubMbPartWidth = SUB_MB_P_TYPE[self.raw_mb_type+1][3]
            self.SubMbPartHeight = SUB_MB_P_TYPE[self.raw_mb_type+1][4]
        else:
            raise Exception("B NOT IMP")
        
        self.mvd_l0 = np.zeros(shape=(self.NumSubMbPart, 2))
        self.mvd_l1 = np.zeros(shape=(self.NumSubMbPart, 2))
        pass





class Macroblock:
    def __init__(self, rbsp:RBSPBits, slice_data:H264SliceData):
        self.rbsp = rbsp
        self.sheader =  slice_data.header
        self.sps = slice_data.sps
        self.pps = slice_data.pps
        self.CurrMbAddr = slice_data.CurrMbAddr
        self.MBAFF = slice_data.MBAFF
        self.slice_data = slice_data

        self.cavlc = None
        self.cabac = None
        self.slice_type = self.sheader.slice_type
        self.transform_8x8_mode_flag = self.pps.transform_8x8_mode_flag
        self.transform_size_8x8_flag = 0

        self.slice_data.mbs.append(self)
        self.blocks = []
        self.ChromaACLevelCrBlocks = []
        self.ChromaACLevelCbBlocks = []
        self.ChromaDCLevelBlocks = []
        self.coded_block_pattern = None
        pass

    def skip_mb(self):
        for i in range(16):
            self.blocks.append(block(0))
        for i in range(4):
            self.ChromaACLevelCbBlocks.append(block(0))
            self.ChromaACLevelCrBlocks.append(block(0))


    def dec(self):
        if not self.pps.entropy_coding_mode_flag:
            self.cavlc = H264CAVLCDec(self.rbsp)
            self.raw_mb_type = self.rbsp.ue()
        else:
            self.cabac = H264CABACDec(self.sheader, self.sps, self.pps, self.rbsp)
            self.raw_mb_type = ae()

        self.mb_type = self.MbTypeName()
        if self.slice_type == 'B' or self.slice_type == "P":
            self.NumMbPart = self.num_mb_part() 
        self.CodedBlockPatternLuma = self.coded_block_pattern_luma()
        self.CodedBlockPatternChroma = self.coded_block_pattern_chroma()


        if self.mb_type == 'I_PCM':
            while True:
                if self.rbsp.byte_aligned():
                    break
                self.rbsp.f(1)
            
            self.pcm_alignment_zero_bit = self.rbsp.f(1)
            self.pcm_sample_luma = []
            self.pcm_sample_chroma = []
            for i in range (256):
                v = self.sps.BitDepthY
                self.pcm_sample_luma.append(self.rbsp.u(v))
            for i in range ( 2 * self.sps.MbWidthC * self.sps.MbHeightC):
                v = self.sps.BitDepthC
                self.pcm_sample_chroma.append(self.rbsp.u(v))
        else:
            noSubMbPartSizeLessThan8x8Flag = 1
            self.MbPartPredMode = self.mb_part_pred_mode(0)

            if self.mb_type != 'I_NxN' and self.MbPartPredMode != 'Intra_16x16' and self.NumMbPart == 4:
                self.sub_mb_pred()
                for mbPartIdx in range(4):
                    if self.sub_mbs[mbPartIdx].type_name != 'B_Direct_8x8':
                        if self.sub_mbs[mbPartIdx].NumSubMbPart > 1:
                            noSubMbPartSizeLessThan8x8Flag = 0
                    elif not self.sps.direct_8x8_inference_flag:
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
                    inter = True
                    if 'Intra' in self.MbPartPredMode:
                        inter = False
                    self.coded_block_pattern = self.rbsp.me(self.sps.ChromaArrayType, inter= inter)
                else:
                    self.coded_block_pattern = self.cabac.ae()
                
                self.CodedBlockPatternLuma = self.coded_block_pattern % 16
                self.CodedBlockPatternChroma = self.coded_block_pattern // 16
                
                if ((self.CodedBlockPatternLuma  > 0) and 
                    (self.transform_8x8_mode_flag == 1) and (self.mb_type != 'I_NxN') and (noSubMbPartSizeLessThan8x8Flag == 1) and
                    (self.mb_type != 'B_Direct_16x16' or self.sps['direct_8x8_inference_flag'])):
                    if self.cavlc != None:
                        self.transform_size_8x8_flag = self.cavlc.rbsp.u(1)
                    else:
                        self.transform_size_8x8_flag = self.cabac.ae()
            if ((self.CodedBlockPatternLuma > 0) or 
                (self.CodedBlockPatternChroma > 0) or 
                (self.MbPartPredMode == 'Intra_16x16')):
                if self.cavlc != None:
                    self.mb_qp_delta = self.cavlc.rbsp.se()
                else:
                    self.mb_qp_delta = self.cabac.ae()
                self.residual(0, 15)
            else:
                for i in range(16):
                    self.blocks.append(block(0))
                for i in range(4):
                    self.ChromaACLevelCbBlocks.append(block(0))
                    self.ChromaACLevelCrBlocks.append(block(0))

    def sub_mb_pred(self):
        subMbs = []
        for mbPartIdx in range(4):
            sub_mb_type = self.rbsp.ue()
            subMb = SubMb(sub_mb_type, self.slice_type)
            subMbs.append(subMb)
        
        self.sub_mbs = subMbs
        
        for mbPartIdx in range(4):
            if ((self.sheader.num_ref_idx_l0_active_minus1 > 0 or self.slice_data.mb_field_decoding_flag != self.sheader.field_pic_flag) and
                self.mb_type != 'P_8x8ref0' and subMbs[mbPartIdx].type_name != "B_Direct_8x8" and subMbs[mbPartIdx].SubMbPredMode != 'Pred_L1'):
                subMbs[mbPartIdx].ref_idx_l0 = self.rbsp.te(self.sheader.num_ref_idx_l0_active_minus1)
        for mbPartIdx in range(4):
            if ((self.sheader.num_ref_idx_l1_active_minus1 > 0 or self.slice_data.mb_field_decoding_flag != self.sheader.field_pic_flag) and
                subMbs[mbPartIdx].type_name != 'B_Direct_8x8' and subMbs[mbPartIdx].SubMbPredMode != 'Pred_L0'):
                subMbs[mbPartIdx].ref_idx_l1 = self.rbsp.te(self.sheader.num_ref_idx_l1_active_minus1)
        
        for mbPartIdx in range(4):
            if subMbs[mbPartIdx].type_name != 'B_Direct_8x8' and subMbs[mbPartIdx].SubMbPredMode != 'Pred_L1':
                for subMbPartIdx  in range(subMbs[mbPartIdx].NumSubMbPart):
                    for compIdx in range(2):
                        subMbs[mbPartIdx].mvd_l0[subMbPartIdx][compIdx] = self.rbsp.se()
        
        for mbPartIdx in range(4):
            if subMbs[mbPartIdx].type_name != "B_Direct_8x8" and subMbs[mbPartIdx].SubMbPredMode != 'Pred_L0':
                for subMbPartIdx in range(subMbs[mbPartIdx].NumSubMbPart):
                    for compIdx in range(2):
                        subMbs[mbPartIdx].mvd_l1[subMbPartIdx][compile] = self.rbsp.se()



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
            if self.sps.ChromaArrayType == 1 or self.sps.ChromaArrayType == 2:
                if self.cavlc != None:
                    self.intra_chroma_pred_mode = self.rbsp.ue()
                else:
                    self.intra_chroma_pred_mode = self.cabac.ae()
        elif self.MbPartPredMode != 'Direct':
            self.ref_idx_l0 = []
            self.ref_idx_l1 = []
            self.mvd_l0 = np.zeros(shape=(2, 1), dtype=np.int32)
            self.mvd_l1 = np.zeros(shape=(2, 1), dtype=np.int32)
            for mbPartIdx in range(self.NumMbPart):
                if ((self.sheader.num_ref_idx_l0_active_minus1 > 0 or self.slice_data.mb_field_decoding_flag != self.sheader.field_pic_flag) and  
                    self.MbPartPredMode != 'Pred_L1'):
                    self.ref_idx_l0.append( self.rbsp.te(self.sheader.num_ref_idx_l0_active_minus1))
            for mbPartIdx in range(self.NumMbPart):
                if ((self.sheader.num_ref_idx_l1_active_minus1 > 0 or self.slice_data.mb_field_decoding_flag != self.sheader.field_pic_flag) and  
                    self.MbPartPredMode != 'Pred_L1'):
                    self.ref_idx_l1.append( self.rbsp.te(self.num_ref_idx_l1_active_minus1))
            for mbPartIdx in range(self.NumMbPart):
                if self.MbPartPredMode != 'Pred_L1':
                    for compIdx in range(2):
                        self.mvd_l0[compIdx] = self.rbsp.se()
            for mbPartIdx in range(self.NumMbPart):
                if self.MbPartPredMode != 'Pred_L0':
                    for compIdx in range(2):
                        self.mvd_l1[compIdx] = self.rbsp.se()

    def residual(self, startIdx, endIdx):
        if self.cavlc != None:
            self.residual_block = self.residual_block_cavlc
        else:
            self.residual_block = None
        
        self.Intral16x16DClevel = np.zeros(shape=(16), dtype=np.int32)
        self.Intral16x16AClevel = np.zeros(shape=(16,16), dtype=np.int32)
        self.LumaLevel4x4 = np.zeros(shape=(16,16), dtype=np.int32)
        self.LumaLevel8x8 = None
        self.startIdx = startIdx
        self.endIdx = endIdx

        self.residual_luma(self.Intral16x16DClevel, self.Intral16x16AClevel, self.LumaLevel4x4, self.LumaLevel8x8, self.startIdx, self.endIdx)

        if self.sps.ChromaArrayType in [1, 2]:
            NumC8x8 = 4 // (self.sps.SubWidthC * self.sps.SubHeightC)
            self.ChromaDCLevel = np.zeros(shape=(2 , 4 * NumC8x8), dtype=np.int32)
            for iCbCr in range(2):
                if ((self.CodedBlockPatternChroma & 3) and startIdx == 0):

                    nC = self.cal_nC('ChromaDCLevel', 0, iCbCr)
                    coeff_token, vals = self.cavlc.ce_coeff_token(nC)
                    self.coeff_token = coeff_token
                    self.TrailingOnes = vals[0]
                    self.TotalCoeff = vals[1]
                    b = block(self.TotalCoeff)
                    self.ChromaDCLevelBlocks.append(b)

                    self.residual_block(self.ChromaDCLevel[iCbCr], 0, 4*NumC8x8-1, 4*NumC8x8)

                else:
                    for i in range(4*NumC8x8):
                        self.ChromaDCLevel[iCbCr][i] = 0

            self.ChromaACLevel = np.zeros(shape=(2, NumC8x8*4, 15), dtype=np.int32)
            for iCbCr in range(2):
                for i8x8 in range (NumC8x8):
                    for i4x4 in range(4):
                        if self.CodedBlockPatternChroma & 2:
                            idx = i8x8 * NumC8x8 + i4x4
                            nC = self.cal_nC('ChromaACLevel', idx, iCbCr)
                            coeff_token, vals = self.cavlc.ce_coeff_token(nC)
                            self.coeff_token = coeff_token
                            self.TrailingOnes = vals[0]
                            self.TotalCoeff = vals[1]
                            b = block(self.TotalCoeff)
                            if iCbCr == 0:
                                self.ChromaACLevelCbBlocks.append(b)
                            else:
                                self.ChromaACLevelCrBlocks.append(b)

                            self.residual_block(self.ChromaACLevel[iCbCr][i8x8*4+i4x4], max(0, startIdx-1), endIdx-1, 15)
                        else:
                            if iCbCr == 0:
                                self.ChromaACLevelCbBlocks.append(block(0))
                            else:
                                self.ChromaACLevelCrBlocks.append(block(0))
                            for i in range(15):
                                self.ChromaACLevel[iCbCr][i8x8*4+i4x4][i] = 0
        elif self.sps.ChromaArrayType == 3:
            self.CbLevel4x4 = np.zeros(shape=(16,16), dtype=np.int32)
            self.CbLevel8x8 = np.zeros(shape=(16,16), dtype=np.int32)

            self.CrLevel4x4 = np.zeros(shape=(16,16), dtype=np.int32)
            self.CrLevel8x8 = np.zeros(shape=(16,16), dtype=np.int32)

            self.residual_luma(self.Intral16x16DClevel, self.Intral16x16AClevel, self.CbLevel4x4, self.CbLevel8x8, startIdx, endIdx)
            self.residual_luma(self.Intral16x16DClevel, self.Intral16x16AClevel, self.CrLevel4x4, self.CrLevel8x8, startIdx, endIdx)


    def residual_luma(self, i16x16DClevel, i16x16AClevel, level4x4, level8x8, startIdx, endIdx):
        if startIdx == 0 and self.MbPartPredMode == 'Intra_16x16':
            nC = self.cal_nC('Intra16x16DCLevel', 0)
            coeff_token, vals = self.cavlc.ce_coeff_token(nC)
            self.coeff_token = coeff_token
            self.TrailingOnes = vals[0]
            self.TotalCoeff = vals[1]
            b = block(self.TotalCoeff)
            #self.blocks.append(b)
            self.residual_block(i16x16DClevel, 0, 15, 16)
        for i8x8 in range(4):
            if (not self.transform_size_8x8_flag) or self.cavlc != None:
                for i4x4 in range(4):
                    if self.CodedBlockPatternLuma & (1 << i8x8):
                        if self.MbPartPredMode == 'Intra_16x16':
                            idx  = i8x8*4+i4x4
                            nC = self.cal_nC('Intra16x16ACLevel', idx)
                            coeff_token, vals = self.cavlc.ce_coeff_token(nC)
                            self.coeff_token = coeff_token
                            self.TrailingOnes = vals[0]
                            self.TotalCoeff = vals[1]
                            b = block(self.TotalCoeff)
                            self.blocks.append(b)
                            self.residual_block(i16x16AClevel[i8x8*4+i4x4], max(0, startIdx -1), endIdx-1, 15)
                        else:
                            luma4x4BlkIdx = i8x8 * 4 + i4x4
                            #xDyD = GetxDyD('A', self.mb_type)
                            #blkA = h264scan.derivation_process_neighbouring_4x4_luma_blocks(luma4x4BlkIdx,xDyD[0], xDyD[1])
                            #xDyD = GetxDyD('B', self.mb_type)
                            #blkB = h264scan.derivation_process_neighbouring_4x4_luma_blocks(luma4x4BlkIdx,xDyD[0], xDyD[1])
                            nC = self.cal_nC('LumaLevel4x4', luma4x4BlkIdx)
                            coeff_token, vals = self.cavlc.ce_coeff_token(nC)
                            self.coeff_token = coeff_token
                            self.TrailingOnes = vals[0]
                            self.TotalCoeff = vals[1]
                            b = block(self.TotalCoeff)
                            self.blocks.append(b)
                            

                            self.residual_block(level4x4[i8x8*4+i4x4], startIdx, endIdx, 16)
                    elif self.MbPartPredMode == 'Intra_16x16':
                        b = block(0)
                        self.blocks.append(b)
                        for i in range(15):
                            i16x16AClevel[i8x8*4 + i4x4][i] = 0
                    else:
                        for i in range(16):
                            level4x4[i8x8 * 4 + i4x4][i] = 0
                        b = block(0)
                        self.blocks.append(b)
                    if self.cavlc != None and self.transform_size_8x8_flag:
                        for i in range(16):
                            level8x8[i8x8][4*i+i4x4] = level4x4[i8x8*4 + i4x4][i]
            elif self.CodedBlockPatternLuma & (1 << i8x8):
                self.residual_block(level8x8[i8x8], 4 * startIdx, 4 * endIdx + 3, 64)
            else:
                for i in range(64):
                    level8x8[i8x8][i] = 0
    
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
                key, total_zeros = self.cavlc.ce_total_zeros(tzVlcIndex, maxNumCoeff)
                zerosLeft = total_zeros

            runVal = np.zeros(shape=(self.TotalCoeff), dtype=np.int32)
            for i in range (self.TotalCoeff - 1):
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
            
        #print("done residual block cavlc")
        pass

    def residual_block_cabac(self, coeffLevel, startIdx, endIdx, maxNumCoeff):
        pass

    
    def TransIType(self, cal_mb_type):
        i_map = I_SLICE_TYPE[cal_mb_type]
        if cal_mb_type == 0:
            if self.transform_8x8_mode_flag == 1:
                return i_map[1]
            else:
                return i_map[0]
        return i_map
    

    def GetMbTypeMap(self):
        mb_type = self.raw_mb_type
        slice_type = self.slice_type
        if slice_type == 'I':
            if mb_type == 0:
                if self.transform_8x8_mode_flag == 1:
                    return I_SLICE_TYPE[mb_type][1]
                else:
                    return I_SLICE_TYPE[mb_type][0]
            return I_SLICE_TYPE[mb_type]
        if slice_type == 'SI':
            if mb_type == 0:
                return SI_SLICE_TYPE[mb_type]
            else:
                return self.TransIType(mb_type - 1)
        if slice_type == 'P' or slice_type == 'SP':
            if mb_type < 5:
                return P_SP_SLICE_TYPE[mb_type]
            else:
                return self.TransIType(mb_type - 5)
        if slice_type == 'B':
            if mb_type < 23:
                return B_SLICES_MB_TYPE[mb_type]
            else:
                return self.TransIType(mb_type - 23)

    def MbTypeName(self):
        return  self.GetMbTypeMap()[0]


    def mb_part_pred_mode(self, param):
        slice_map = self.GetMbTypeMap()
        idx = 2
        if self.slice_type == "SI":
            idx = 1
        if param == 1:
            if slice_type == 'I' or slice_type == 'SI':
                raise Exception("slice type error, this slice no MbpartPredMode(mb_type, 1) define")
            idx = 3
        return slice_map[idx]

    def num_mb_part(self):
        return self.GetMbTypeMap()[1]

    def coded_block_pattern_luma(self):
        if (self.slice_type == 'P' and self.raw_mb_type < len(P_SP_SLICE_TYPE)) or (self.slice_type == 'B' and self.raw_mb_type < len(B_SLICES_MB_TYPE)) :
            return 0
        slice_map = self.GetMbTypeMap()
        return slice_map[5]

    def coded_block_pattern_chroma(self):
        if (self.slice_type == 'P' and self.raw_mb_type < len(P_SP_SLICE_TYPE)) or (self.slice_type == 'B' and self.raw_mb_type < len(B_SLICES_MB_TYPE)) :
            return 0
        slice_map = self.GetMbTypeMap()
        return slice_map[4]
    
    def cal_nC(self, level, idx, iCbCr=0):
        if level == 'ChromaDCLevel':
            if self.sps.ChromaArrayType == 1:
                return -1
            else:
                return -2
        elif level == 'Intra16x16DCLevel':
            luma4x4BlkIdx = 0
            idx = luma4x4BlkIdx
        elif level == 'CbIntra16x16DCLevel':
            cb4x4BlkIdx = 0
            idx = cb4x4BlkIdx
        elif level == 'CrIntra16x16DCLevel':
            cr4x4BlkIdx = 0
            idx = cr4x4BlkIdx
        
        blkA = None
        blkB = None
        nA = 0
        nB = 0
        nC = 0

        if level in ['Intra16x16DCLevel', 'Intra16x16ACLevel', 'LumaLevel4x4']:
            xD, yD = self.xDyD('A')
            x, y = h264scan.inverse_4x4_luma_block_scanning_process(idx)
            xN, yN = x + xD, y+yD
            addr, xW, yW = self.neighbouring_locations(xN, yN)
            blkidx = None 
            if addr != None:
                blkidx = h264scan.luma_block_indices_4x4(xW, yW)
            if addr == None:
                nA = None 
            else:
                blkA = addr
                nA = self.slice_data.mbs[addr].blocks[blkidx].TotalCoeff

            xD, yD = self.xDyD('B')
            x, y = h264scan.inverse_4x4_luma_block_scanning_process(idx)
            xN, yN = x + xD, y+yD
            addr, xW, yW = self.neighbouring_locations(xN, yN)
            blkidx = None 
            if addr != None:
                blkidx = h264scan.luma_block_indices_4x4(xW, yW)
            if addr == None:
                blkB = None 
            else:
                blkB = addr
                nB  = self.slice_data.mbs[addr].blocks[blkidx].TotalCoeff

        elif level in ['CbIntra16x16DCLevel', 'CbIntra16x16ACLevel', 'CbLevel4x4']:
            raise Exception("NOT IMP")
        elif level in ['CrIntra16x16DCLevel', 'CrIntra16x16ACLevel', 'CrLevel4x4']:
            raise Exception("NOT IMP")
        elif level in ['ChromaACLevel']:
            xD, yD = self.xDyD("A")
            x, y = h264scan.inverse_4x4_chroma_block_scanning_process(idx)
            xN, yN = x+xD, y+yD
            blkA, xW,yW = self.neighbouring_locations(xN, yN, False)
            nA = None

            if blkA != None:
                blkidx = h264scan.chroma_block_indices_4x4(xW, yW)
                if iCbCr == 0:
                    nA = self.slice_data.mbs[blkA].ChromaACLevelCbBlocks[blkidx].TotalCoeff
                else:
                    nA = self.slice_data.mbs[blkA].ChromaACLevelCrBlocks[blkidx].TotalCoeff

            xD, yD = self.xDyD("B")
            x, y = h264scan.inverse_4x4_chroma_block_scanning_process(idx)
            xN, yN = x+xD, y+yD
            blkB, xW,yW = self.neighbouring_locations(xN, yN, False)
            nB = None

            if blkB != None:
                blkidx = h264scan.chroma_block_indices_4x4(xW, yW)
                if iCbCr == 0:
                    nB = self.slice_data.mbs[blkB].ChromaACLevelCbBlocks[blkidx].TotalCoeff
                else:
                    nB = self.slice_data.mbs[blkB].ChromaACLevelCrBlocks[blkidx].TotalCoeff

        
        if blkA != None and blkB != None:
            nC = (nA + nB + 1) >> 1
        elif blkA != None:
            nC = nA
        elif blkB != None:
            nC = nB
        return nC


    def xDyD(self, N):
        if N == "A":
            return (-1, 0)
        if N == "B":
            return (0, -1)
        if N == "C":
            prePartWidth = 0
            if self.mb_type in ['P_Skip', 'B_Direct_16x16']:
                prePartWidth = 16
            elif mb_type == 'B_8x8':
                if self.currSubMbType == "B_Direct_8x8":
                    prePartWidth = 16
                else:
                    prePartWidth = self.SubMbPartWidth
            elif mb_type in ['P_8x8', 'P_8x8ref0']:
                prePartWidth = self.SubMbPartWidth
            else:
                prePartWidth = MbPartWidth(mb_type)
            return (prePartWidth, -1)
        if N == "D":
            return (-1, -1)
    
    def neighbouring_locations(self, xN, yN, luma_invoke = True):
        maxW = 16
        maxH = 16
        if not luma_invoke:
            maxW = self.sps.MbWidthC
            maxH = self.sps.MbHeightC
        if not self.MBAFF:
            mbAddrN, xW, xY = self.neighbouring_locations_non_MBAFF(xN, yN, maxW, maxH)
        else:
            raise Exception("NOT IMP")
        
        return mbAddrN, xW, xY
        
        


    def neighbouring_locations_non_MBAFF(self, xN, yN, maxW, maxH):
        t = 'na'
        addr = None
        if xN < 0 and yN < 0:
            t = 'D'

        elif xN < 0 and yN >= 0 and yN < maxH:
            t = 'A'
        elif xN >= 0 and xN < maxW and yN < 0 :
            t = 'B'
        elif xN >= 0 and xN < maxW and yN >= 0 and yN < maxH:
            t = 'S'
        elif xN >= maxW and yN < 0:
            t = 'C'
        else:
            t = 'na'
        addr = self.neighbouring_macroblock_addr(t)

        if t == 'na' or addr == None:
            return None, None, None
        
        xW = (xN + maxW) % maxW
        yW = (yN + maxH) % maxH
        
        return addr, xW, yW

    def neighbouring_macroblock_addr(self, t):
        if t == 'S':
            return self.CurrMbAddr

        if t == 'A':
            addr = self.CurrMbAddr - 1
            if self.CurrMbAddr % self.sps.PicWidthInMbs == 0:
                return None
            return addr
        if t == 'B':
            addr = self.CurrMbAddr - self.sps.PicWidthInMbs
            if addr < 0:
                return None
            return addr
        if t == 'C':
            addr = self.CurrMbAddr - self.sps.PicWidthInMbs + 1
            if (self.CurrMbAddr+1)%self.sps.PicWidthInMbs == 0:
                return None
            return addr
        if t == 'D':
            if self.CurrMbAddr % self.sps.PicWidthInMbs == 0:
                return None
            addr = self.CurrMbAddr - self.sps.PicWidthInMbs - 1
            if addr < 0:
                return None
            return addr
        return None
