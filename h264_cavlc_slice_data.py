from rbsp import RBSPBits
import h264_mb
from h264_slice_header import H264SliceHeader


class H264SliceData:
    def __init__(self, header:H264SliceHeader):
        self.rbsp = header.rbsp
        self.header = header

    def dec_slice(self):
        self.MbaffFrameFlag = 1 if self.header.sps.mb_adaptive_frame_filed_flag and self.header.field_pic_flag else 0
        self.CurrMbAddr = self.header.first_mb_in_slice * ( 1 + self.MbaffFrameFlag)
        moreDataFlag = True
        prevMbSkipped = False
        while True:
            if self.header.slice_type != 'I' and self.header.slice_type != 'SI':
                mb_skip_run = self.rbsp.ue()
                prevMbSkipped = mb_skip_run > 0
                for i in range(mb_skip_run):
                    CurrMbAddr = self.NextMbAddress(CurrMbAddr)
                if mb_skip_run > 0 :
                    moreDataFlag = self.rbsp.more_rbsp_data()
                
            if moreDataFlag:
                if self.MbaffFrameFlag and (CurrMbAddr%2 == 0 and (CurrMbAddr%2 == 1 and prevMbSkipped)):
                    self.mb_field_decoding_flag = self.rbsp.u(1)
                    self.header.mb_field_decoding_flag = self.mb_field_decoding_flag
                mb = h264_mb.Macroblock(self.header, self.header.sps, self.header.pps, self.header.rbsp)
                mb.dec()

            moreDataFlag = self.rbsp.more_rbsp_data()
            CurrMbAddr = self.NextMbAddress(CurrMbAddr)
            if not moreDataFlag :
                break
    
    def NextMbAddress(self, n):
        i = n + 1
        # while True:
        #     if i < h264sps.PicSizeInMapUnits
        pass

