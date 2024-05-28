from rbsp import RBSPBits
import h264_mb
from h264_slice_header import H264SliceHeader
import h264_slice_data
import numpy as np


class H264CavlcSlice:
    def __init__(self, header:H264SliceHeader):
        self.rbsp = header.rbsp
        self.header = header
        self.slice_group_map()

    def dec_slice(self):
        self.MbaffFrameFlag = 1 if self.header.sps.mb_adaptive_frame_filed_flag and self.header.field_pic_flag else 0
        self.CurrMbAddr = self.header.first_mb_in_slice * ( 1 + self.MbaffFrameFlag)

        self.slice_data = h264_slice_data.H264SliceData(self.header.sps, self.header.pps, self.header, self.CurrMbAddr, self.MbaffFrameFlag)

        moreDataFlag = True
        prevMbSkipped = False
        while True:
            if self.header.slice_type != 'I' and self.header.slice_type != 'SI':
                mb_skip_run = self.rbsp.ue()
                prevMbSkipped = mb_skip_run > 0
                for i in range(mb_skip_run):
                    mb = h264_mb.Macroblock(self.header.rbsp, self.slice_data)
                    mb.skip_mb()
                    self.CurrMbAddr = self.NextMbAddress(self.CurrMbAddr)
                    self.slice_data.CurrMbAddr = self.CurrMbAddr
                if mb_skip_run > 0 :
                    moreDataFlag = self.rbsp.more_rbsp_data()
                
            if moreDataFlag:
                if self.MbaffFrameFlag and (self.CurrMbAddr%2 == 0 and (self.CurrMbAddr%2 == 1 and prevMbSkipped)):
                    self.mb_field_decoding_flag = self.rbsp.u(1)
                    self.slice_data.mb_field_decoding_flag = self.mb_field_decoding_flag
                mb = h264_mb.Macroblock(self.header.rbsp, self.slice_data)
                mb.dec()

            moreDataFlag = self.rbsp.more_rbsp_data()
            self.CurrMbAddr = self.NextMbAddress(self.CurrMbAddr)
            self.slice_data.CurrMbAddr = self.CurrMbAddr
            if not moreDataFlag :
                break
    
    def NextMbAddress(self, n):
        i = n + 1
        while True:
            if not (i < self.header.sps.PicSizeInMapUnits and self.mapUnitTosliceGroupMap[i] != self.mapUnitTosliceGroupMap[n]):
                break

            i+=1
        return i
        
    def slice_group_map(self):
        if self.header.pps.num_slice_groups_minus1 == 1 and (self.header.pps.slice_group_map_type in [3, 4, 5]):
            raise Exception("NOT IMP")
        if self.header.pps.num_slice_groups_minus1 == 0:
            self.mapUnitTosliceGroupMap = np.zeros(self.header.sps.PicSizeInMapUnits)
        else:
            raise Exception("NOT IMP")


        

