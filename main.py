from bitstring import BitArray, BitStream
from rbsp import RBSPBits
import h264_sps
import h264_pps
import h264_slice


file = open("res/test.h264", "rb")

nalus = list(BitArray(file).split('0x000001', bytealigned=True))[1:]
spsparam = None
ppsparam = None
for nalu in nalus :
    #todo nalu need check emulation_prevention_three_byte
    nalu.replace('0x000003', '0x0000', bytealigned=True)
    rbsp = RBSPBits(BitStream(nalu[24:]))
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
        spsparam = h264_sps.H264SPS(rbsp)
        spsparam.dec()
    elif params['nal_unit_type'] == 8:
        ppsparam = h264_pps.H264PPS(rbsp)
        ppsparam.dec()
        print("pps")
    elif params['nal_unit_type'] == 5:
        slice_data =  h264_slice.H264Slice(params, spsparam, ppsparam, rbsp)
        slice_data.dec()
        print("IDR")

    elif params['nal_unit_type'] in [1,4]:
        h264slice.slice_layer_without_partitioning_rbsp(params, spsparam, ppsparam, rbsp)
        print("PIC")
    

print("test")