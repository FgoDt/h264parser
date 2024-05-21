from rbsp import RBSPBits
Extended_SAR = 255

def dec_hrd_parameters(rbsp:RBSPBits):
    hrd = {
        'cpb_cnt_minus1':rbsp.ue(),
        'bit_rate_scale':rbsp.u(4),
        'cpb_rate_scale':rbsp.u(4)
    }
    bit_rate_value_minus1 = []
    cpb_size_value_minus1 = []
    cbr_flag = []
    for SchedSelIdx in range(hrd['cpb_cnt_minus1'] + 1):
        bit_rate_value_minus1.append(rbsp.ue())
        cpb_size_value_minus1.append(rbsp.ue())
        cbr_flag.append(rbsp.u(1))
    hrd['bit_rate_value_minus1'] = bit_rate_value_minus1
    hrd['cpb_size_value_minus1'] = cpb_size_value_minus1
    hrd['cbr_flag'] = cbr_flag
    hrd['inital_cpb_removal_delay_length_minus1'] = rbsp.u(5)
    hrd['cpb_removal_delay_length_minus1'] = rbsp.u(5)
    hrd['dpb_output_delay_length_minus1'] = rbsp.u(5)
    hrd['time_offset_length'] = rbsp.u(5)
    return hrd



def dec_vui_parameters(rbsp: RBSPBits):
    vui = {}
    vui['aspect_ratio_info_present_flag'] = rbsp.u(1)
    if vui['aspect_ratio_info_present_flag'] == 1:
        vui['aspect_ratio_idc'] = rbsp.u(8)
        if vui['aspect_ratio_idc'] == Extended_SAR :
            vui[sar_width] = rbsp.u(16)
            vui[sar_height] = rbsp.u(16)
    vui['overscan_info_present_flag']=rbsp.u(1)
    if vui['overscan_info_present_flag'] == 1:
        vui['overscan_appropriate_flag'] = rbsp.u(1)
    vui['video_signal_type_present_flag'] = rbsp.u(1)
    if vui['video_signal_type_present_flag'] == 1:
        vui['video_format'] = rbsp.u(3)
        vui['video_full_range_flag'] = rbsp.u(1)
        vui['colour_description_present_flag'] = rbsp.u(1)
        if vui['colour_description_present_flag'] == 1:
            vui['colour_primaries'] = rbsp.u(8)
            vui['transfer_characteristics'] = rbsp.u(8)
            vui['matix_coefficients'] = rbsp.u(8)
    vui['chroma_loc_info_present_flag'] = rbsp.u(1)
    if vui['chroma_loc_info_present_flag'] == 1:
        vui['chroma_sample_loc_type_top_field'] = rbsp.ue()
        vui['chroma_sample_loc_type_bottom_field'] = rbsp.ue()
    vui['timing_info_present_flag'] = rbsp.u(1)
    if vui['timing_info_present_flag'] == 1:
        vui['num_units_in_tick'] = rbsp.u(32)
        vui['time_scale'] = rbsp.u(32)
        vui['fixed_frame_rate_flag'] = rbsp.u(1)
    vui['nal_hrd_parameters_present_flag'] = rbsp.u(1)
    if vui['nal_hrd_parameters_present_flag'] == 1:
        vui['nal_hrd_param'] = dec_hrd_parameters(rbsp)
    vui['vcl_hrd_parameters_present_flag'] = rbsp.u(1)
    if vui['vcl_hrd_parameters_present_flag'] == 1:
        vui['vcl_hrd_param'] = dec_hrd_parameters(rbsp)
    if vui['vcl_hrd_parameters_present_flag'] or vui['nal_hrd_parameters_present_flag'] :
        vui['low_delay_hrd_flag'] = rbsp.u(1)
    
    vui['pic_struct_present_flag'] = rbsp.u(1)
    vui['bitstream_restriction_flag'] = rbsp.u(1)
    if vui['bitstream_restriction_flag'] == 1:
        vui['montion_vectors_over_pic_boundaries_flag'] = rbsp.u(1)
        vui['max_bytes_per_pic_denom'] = rbsp.ue()
        vui['max_bits_per_mb_denom'] = rbsp.ue()
        vui['log2_max_mv_length_horizontal'] = rbsp.ue()
        vui['log2_max_mv_length_vertical'] = rbsp.ue()
        vui['max_num_reorder_frames'] = rbsp.ue()
        vui['max_dec_frame_buffering'] = rbsp.ue()
    return vui
    

def dec_seq_parameter_set_data(params, rbsp: RBSPBits):
    sps = {
        'profile_idc':rbsp.u(8),
        'constraint_set0_flag':rbsp.u(1),
        'constraint_set1_flag':rbsp.u(1),
        'constraint_set2_flag':rbsp.u(1),
        'constraint_set3_flag':rbsp.u(1),
        'constraint_set4_flag':rbsp.u(1),
        'constraint_set5_flag':rbsp.u(1),
        'reserved_zero_2bits':rbsp.u(2),
        'level_idc':rbsp.u(8),
        'seq_parameter_set_id':rbsp.ue(),
    }
    set_default(sps)
    profile_idc = sps['profile_idc']
    if (profile_idc == 100 or profile_idc == 110 or 
        profile_idc == 122 or profile_idc == 244 or 
        profile_idc == 44  or profile_idc == 83  or 
        profile_idc == 128 or profile_idc == 138 or 
        profile_idc == 139 or profile_idc == 134 or profile_idc == 135):
        sps['chroma_format_idc'] = rbsp.ue()
        if sps['chroma_format_idc'] == 3:
            sps['separate_colour_plane_flag'] = rbsp.u(1)
        sps['bit_depth_luma_minus8'] = rbsp.ue()
        sps['bit_depth_chroma_minus8'] = rbsp.ue()
        sps['qprime_y_zero_transform_bypass_flag'] = rbsp.u(1)
        sps['seq_scaling_matrix_present_flag'] = rbsp.u(1)
        if sps['seq_scaling_matrix_present_flag']:
            loop = 8 if chroma_format_idc == 3 else 12
            list_flag = []
            for i in range(loop):
                flag = rbsp.u(1)
                list_flag.append(flag)
                if flag != 0:
                    if i < 6 :
                        #TODO scaling_list
                        assert False
                    else:
                        assert False
            sps['seq_scaling_list_present_flag']=list_flag
                    
    sps['log2_max_frame_num_minus4'] = rbsp.ue()
    sps['pic_order_cnt_type'] = rbsp.ue()
    if sps['pic_order_cnt_type'] == 0 :
        sps['log2_max_pic_order_cnt_lsb_minus4'] = rbsp.ue()
    elif sps['pic_order_cnt_type'] == 1:
        sps['delta_pic_order_always_zero_flag'] = rbsp.u(1)
        sps['offset_for_non_ref_pic'] = rbsp.se()
        sps['offset_for_top_to_bottom_field'] = rbsp.se()
        sps['num_ref_frames_in_pic_order_cnt_cycle'] = rbsp.ue()
        offset_for_ref_frames = []
        for i in range(sps['num_ref_frames_in_pic_order_cnt_cycle']):
            offset_for_ref_frames.append(rbsp.se())

    sps['max_num_ref_rames'] = rbsp.ue()
    sps['gaps_in_frame_num_value_allowed_flag'] = rbsp.u(1)
    sps['pic_width_in_mbs_minus1'] = rbsp.ue()
    sps['pic_height_in_map_units_minus1'] = rbsp.ue()
    sps['frame_mbs_only_flag'] = rbsp.u(1)
    if sps['frame_mbs_only_flag'] == 0 :
        sps['mb_adaptive_frame_filed_flag'] = rbsp.u(1)
    sps['direct_8x8_inference_flag'] = rbsp.u(1)
    sps['frame_cropping_flag'] = rbsp.u(1)
    if sps['frame_cropping_flag'] == 1:
        sps['frame_crop_left_offset'] = rbsp.ue()
        sps['frame_crop_right_offset'] = rbsp.ue()
        sps['frame_crop_top_offset'] = rbsp.ue()
        sps['frame_crop_bottom_offset'] = rbsp.ue()
    sps['vui_parameters_present_flag'] = rbsp.u(1)
    if sps['vui_parameters_present_flag'] == 1:
        sps['vui']=dec_vui_parameters(rbsp)
    print(sps)
    return sps

def set_default(sps):
    sps['separate_colour_plane_flag'] = 0
    sps['mb_adaptive_frame_filed_flag'] = 0
    sps['chroma_format_idc'] = 1
    if sps['profile_idc'] == 183:
        sps['chroma_format_idc'] = 0

def PicWidthInMbs(sps):
    return sps['pic_width_in_mbs_minus1'] + 1

def PicWidthInSamplesL(sps):
    return PicWidthInMbs(sps) * 16

def PicWidthInSamplesC(sps):
    return PicWidthInMbs(sps) * MbWidthC(sps)

def MbWidthC(sps):
    return 16//SubWidthC(sps)

def MbHeightC(sps):
    return 16//SubHeightC(sps)

SubWidthCMap = [-1, 2, 2, 1]
SubHeightCMap = [-1, 2, 1, 1]
def SubWidthC(sps):
    return SubWidthCMap[sps['chroma_format_idc']]

def SubHeightC(sps):
    return SubHeightCMap[sps['chroma_format_idc']]

def PicHeightInMapUnits(sps):
    return sps['pic_height_in_map_units_minus1'] + 1

def PicSizeInMapUnits(sps):
    return PicWidthInMbs(sps) * PicHeightInMapUnits(sps)

def BitDepthY(sps):
    return 8 + sps['bit_depth_luma_minus8']

def QpBdOffsetY(sps):
    return 6 * sps['bit_depth_luma_minus8']

def BitDepthC(sps):
    return 8 + sps['bit_depth_chroma_minus8']

def QpBdOffsetC(sps):
    return 6 * sps['bit_depth_chroma_minus8']

def RawMbBits(sps):
    return 256 * BitDepthY(sps) + 2 * MbWidthC * MbHeightC * BitDepthC