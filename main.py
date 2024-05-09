from bitstring import BitArray, BitStream
from rbsp import RBSPBits
import sps
import pps


file = open("res/test.h264", "rb")

nalus = list(BitArray(file).split('0x000001', bytealigned=True))[1:]
spsparam = None
ppsparam = None
for nalu in nalus :
    #todo nalu need check emulation_prevention_three_byte
    nalu.replace('0x000003', '0x0000', bytealigned=True)
    rbsp = RBSPBits(BitStream(nalu))
    ret = rbsp.u(24)
    params = {
        "forbidden_zero_bit": rbsp.f(1),
        "nal_ref_idc": rbsp.u(2),
        "nal_unit_type": rbsp.u(5)
    }
    print(params)
    if params['nal_unit_type'] == 6:
        print("sei skip")
        continue
    elif params['nal_unit_type'] == 7:
        print("sps")
        spsparam = sps.dec_seq_parameter_set_data(params=params, rbsp=rbsp)
    elif params['nal_unit_type'] == 8:
        ppsparam = pps.dec_pic_parameter_set(rbsp)
        print("pps")
    elif params['nal_unit_type'] == 5:
        print("IDR")
    elif params['nal_unit_type'] in [1,4]:
        print("PIC")
    

print("test")