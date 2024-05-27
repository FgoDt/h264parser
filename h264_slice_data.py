from h264_pps import H264PPS
from h264_sps import H264SPS
from h264_slice_header import H264SliceHeader

class H264SliceData:
    def __init__(self, sps: H264SPS, pps: H264PPS, header: H264SliceHeader, CurrMbAddr, MBAFF):
        self.mbs = []
        self.sps = sps
        self.pps = pps
        self.header = header
        self.CurrMbAddr = CurrMbAddr
        self.MBAFF = MBAFF
        self.mb_field_decoding_flag = 0
        pass
