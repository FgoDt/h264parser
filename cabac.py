from rbsp import RBSPBits
import math

class CABAC:
    def __init__(rbsp:RBSPBits):
        self.rbsp = rbsp
        self.ctx_inited = False

    def cabac_parsing(self, se):
        if not self.ctx_inited:
            self.init_context_variables()
            self.init_decoding_engine()
        
        bits = self.get_binarization()
        binidx = -1

        for bit in bits :
            binidx += 1
            ctxIdx = self.get_ctxIdx(binidx)
            self.dec_bin(ctxIdx)

        pass

    def init_context_variables(self):
        pass
    
    def init_decoding_engine(self):
        self.codIRange = 0x1fe
        self.codIOffset = self.rbsp.u(9)
        pass

    def get_binarization(self, se):
        self.binIdx = 0
        if se == "mb_skip_flag":
            self.maxBinIdxCtx = 0
            self.ctxIdxOffset = 11
            cMax = 1
            fl_len = cabac_fl_binarization_len(cMax)
            val = 0
            for i in range(fl_len):
                val = val<< 1
                val += rbsp.u(1)
            high_mb_loc = 2 * (cur_mb_addr//2)
            high_mb = mbs[high_mb_loc]

            if MbaffFrameFlag and high_mb['mb_field_decoding_flag']:
                mba = mbAddrA(cur_mb_loc)
                mbb = mbAddrB(cur_mb_loc)
                inc = 0
                if mba != unusable or mba['mb_skip_flag']:
                    inc += 1
                if mbb != unusable or mbb['mb_skip_flag']:
                    inc += 1
                self.ctxIdxInc = inc
            
            self.ctxIdx = self.ctxIdxInc + self.ctxIdxOffset
            self.bypass = False

        pass

    def get_ctxIdx(self, ctxIdxInc):
        self.normal_ctxIdxInc_map = {}
        pass

    def dec_bin(self):
        if self.bypass:
            return self.dec_bypass()
        elif self.ctxIdx == 276:
            return self.dec_terminate()
            
        
        pass
    def dec_bypass(self):
        pass
    def dec_terminate(self):
        pass

    def cabac_binarization_process(se, rbsp: RBSPBits):


def cabac_fl_binarization_len(cmax):
    return math.ceil(math.log2(cmax + 1))



def cabac_mb_skip_flag():
    bin_val =  cabac_binarization_process("mb_skip_flag")

