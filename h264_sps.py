from rbsp import RBSPBits
Extended_SAR = 255
SubWidthCMap = [-1, 2, 2, 1]
SubHeightCMap = [-1, 2, 1, 1]

class H264HRD:
    def __init__(self, rbsp:RBSPBits):
        self.rbsp = rbsp
    
    def dec(self):
        self.cpb_cnt_minus1 = self.rbsp.ue()
        self.bit_rate_scale = self.rbsp.u(4)
        self.cpb_rate_scale = self.rbsp.u(4)

        self.bit_rate_value_minus1 = []
        self.cpb_size_value_minus1 = []
        self.cbr_flag = []

        for SchedSelIdx in range(self.cpb_cnt_minus1 + 1):
            self.bit_rate_value_minus1.append(self.rbsp.ue())
            self.cpb_size_value_minus1.append(self.rbsp.ue())
            self.cbr_flag.append(self.rbsp.u(1))

        self.inital_cpb_removal_delay_length_minus1 = self.rbsp.u(5)
        self.cpb_removal_delay_length_minus1 = self.rbsp.u(5)
        self.dpb_output_delay_length_minus1 = self.rbsp.u(5)
        self.time_offset_length = self.rbsp.u(5)
        pass
    pass

class H264VUI:
    def __init__(self, rbsp:RBSPBits):
        self.rbsp = rbsp
    
    def dec(self):
        self.aspect_ratio_info_present_flag = self.rbsp.u(1)
        if self.aspect_ratio_info_present_flag == 1:
            self.aspect_ratio_idc = self.rbsp.u(8)
            if self.aspect_ratio_idc == Extended_SAR :
                self.sar_width = self.rbsp.u(16)
                self.sar_height = self.rbsp.u(16)
        self.overscan_info_present_flag=self.rbsp.u(1)
        if self.overscan_info_present_flag == 1:
            self.overscan_appropriate_flag = self.rbsp.u(1)
        self.video_signal_type_present_flag = self.rbsp.u(1)
        if self.video_signal_type_present_flag == 1:
            self.video_format = self.rbsp.u(3)
            self.video_full_range_flag = self.rbsp.u(1)
            self.colour_description_present_flag = self.rbsp.u(1)
            if self.colour_description_present_flag == 1:
                self.colour_primaries = self.rbsp.u(8)
                self.transfer_characteristics = self.rbsp.u(8)
                self.matix_coefficients = self.rbsp.u(8)
        self.chroma_loc_info_present_flag = self.rbsp.u(1)
        if self.chroma_loc_info_present_flag == 1:
            self.chroma_sample_loc_type_top_field = self.rbsp.ue()
            self.chroma_sample_loc_type_bottom_field = self.rbsp.ue()
        self.timing_info_present_flag = self.rbsp.u(1)
        if self.timing_info_present_flag == 1:
            self.num_units_in_tick = self.rbsp.u(32)
            self.time_scale = self.rbsp.u(32)
            self.fixed_frame_rate_flag = self.rbsp.u(1)
        self.nal_hrd_parameters_present_flag = self.rbsp.u(1)
        if self.nal_hrd_parameters_present_flag == 1:
            self.nal_hrd_param = H264HRD(self.rbsp)
            self.nal_hrd_param.dec()
        self.vcl_hrd_parameters_present_flag = self.rbsp.u(1)
        if self.vcl_hrd_parameters_present_flag == 1:
            self.vcl_hrd_param = H264HRD(self.rbsp)
            self.vcl_hrd_param.dec()
        if self.vcl_hrd_parameters_present_flag or self.nal_hrd_parameters_present_flag :
            self.low_delay_hrd_flag = self.rbsp.u(1)
    
        self.pic_struct_present_flag = self.rbsp.u(1)
        self.bitstream_restriction_flag = self.rbsp.u(1)
        if self.bitstream_restriction_flag == 1:
            self.montion_vectors_over_pic_boundaries_flag = self.rbsp.u(1)
            self.max_bytes_per_pic_denom = self.rbsp.ue()
            self.max_bits_per_mb_denom = self.rbsp.ue()
            self.log2_max_mv_length_horizontal = self.rbsp.ue()
            self.log2_max_mv_length_vertical = self.rbsp.ue()
            self.max_num_reorder_frames = self.rbsp.ue()
            self.max_dec_frame_buffering = self.rbsp.ue()

class H264SPS:
    def __init__(self, rbsp:RBSPBits):
        self.rbsp = rbsp
        self.separate_colour_plane_flag = 0
        self.mb_adaptive_frame_filed_flag = 0
        self.chroma_format_idc = 1
        self.bit_depth_luma_minus8 = 0
        self.bit_depth_chroma_minus8 = 0
        self.qpprime_y_zero_transform_bypass_flag = 0
    
    def dec(self):
        self.profile_idc = self.rbsp.u(8)
        if self.profile_idc == 183:
            self.chroma_format_idc = 0
        self.constraint_set0_flag = self.rbsp.u(1)
        self.constraint_set1_flag = self.rbsp.u(1)
        self.constraint_set2_flag = self.rbsp.u(1)
        self.constraint_set3_flag = self.rbsp.u(1)
        self.constraint_set4_flag = self.rbsp.u(1)
        self.constraint_set5_flag = self.rbsp.u(1)
        self.reserved_zero_2bits = self.rbsp.u(2)
        self.level_idc = self.rbsp.u(8)
        self.seq_parameter_set_id = self.rbsp.ue()

        profile_idc = self.profile_idc
        if (profile_idc == 100 or profile_idc == 110 or 
            profile_idc == 122 or profile_idc == 244 or 
            profile_idc == 44  or profile_idc == 83  or 
            profile_idc == 128 or profile_idc == 138 or 
            profile_idc == 139 or profile_idc == 134 or profile_idc == 135):
            self.chroma_format_idc = self.rbsp.ue()
            if self.chroma_format_idc == 3:
                self.separate_colour_plane_flag = self.rbsp.u(1)
            self.bit_depth_luma_minus8 = self.rbsp.ue()
            self.bit_depth_chroma_minus8 = self.rbsp.ue()
            self.qpprime_y_zero_transform_bypass_flag = self.rbsp.u(1)
            self.seq_scaling_matrix_present_flag = self.rbsp.u(1)
            if self.seq_scaling_matrix_present_flag:
                loop = 8 if self.chroma_format_idc == 3 else 12
                list_flag = []
                for i in range(loop):
                    flag = self.rbsp.u(1)
                    list_flag.append(flag)
                    if flag != 0:
                        if i < 6 :
                            #TODO scaling_list
                            assert False
                        else:
                            assert False
                self.seq_scaling_list_present_flag=list_flag

        self.log2_max_frame_num_minus4 = self.rbsp.ue()
        self.pic_order_cnt_type = self.rbsp.ue()
        if self.pic_order_cnt_type == 0 :
            self.log2_max_pic_order_cnt_lsb_minus4 = self.rbsp.ue()
        elif self.pic_order_cnt_type == 1:
            self.delta_pic_order_always_zero_flag = self.rbsp.u(1)
            self.offset_for_non_ref_pic = self.rbsp.se()
            self.offset_for_top_to_bottom_field = self.rbsp.se()
            self.num_ref_frames_in_pic_order_cnt_cycle = self.rbsp.ue()
            offset_for_ref_frames = []
            for i in range(self.num_ref_frames_in_pic_order_cnt_cycle):
                offset_for_ref_frames.append(self.rbsp.se())

        self.max_num_ref_rames = self.rbsp.ue()
        self.gaps_in_frame_num_value_allowed_flag = self.rbsp.u(1)
        self.pic_width_in_mbs_minus1 = self.rbsp.ue()
        self.pic_height_in_map_units_minus1 = self.rbsp.ue()
        self.frame_mbs_only_flag = self.rbsp.u(1)
        if self.frame_mbs_only_flag == 0 :
            self.mb_adaptive_frame_filed_flag = self.rbsp.u(1)
        self.direct_8x8_inference_flag = self.rbsp.u(1)
        self.frame_cropping_flag = self.rbsp.u(1)
        if self.frame_cropping_flag == 1:
            self.frame_crop_left_offset = self.rbsp.ue()
            self.frame_crop_right_offset = self.rbsp.ue()
            self.frame_crop_top_offset = self.rbsp.ue()
            self.frame_crop_bottom_offset = self.rbsp.ue()
        self.vui_parameters_present_flag = self.rbsp.u(1)
        if self.vui_parameters_present_flag == 1:
            self.vui=H264VUI(self.rbsp)
            self.vui.dec()
        self.cal_val()
        print(self)
        pass

    def cal_val(self):
        self.PicHeightInMapUnits = self.pic_height_in_map_units_minus1 + 1

        self.FrameHeightInMbs = (2 - self.frame_mbs_only_flag) * self.PicHeightInMapUnits

        #self.PicHeightInMbs = self.FrameHeightInMbs // (1 + self.field_pic_flag)

        self.PicWidthInMbs = self.pic_width_in_mbs_minus1 + 1

        self.PicWidthInSamplesL = self.PicWidthInMbs * 16

        self.SubWidthC = SubWidthCMap[self.chroma_format_idc]
        self.SubHeightC = SubHeightCMap[self.chroma_format_idc]

        self.MbWidthC = 16//self.SubWidthC
        self.MbHeightC = 16//self.SubHeightC

        self.PicWidthInSamplesC = self.PicWidthInMbs * self.MbWidthC

        self.PicSizeInMapUnits = self.PicWidthInMbs * self.PicHeightInMapUnits

        self.BitDepthY = 8 + self.bit_depth_luma_minus8

        self.QpBdOffsetY = 6 * self.bit_depth_luma_minus8

        self.BitDepthC = 8 + self.bit_depth_chroma_minus8

        self.QpBdOffsetC = 6 * self.bit_depth_chroma_minus8

        self.RawMbBits = 256 * self.BitDepthY + 2 * self.MbWidthC * self.MbHeightC * self.BitDepthC 

        self.ChromaArrayType = 0 if self.separate_colour_plane_flag == 1 else self.chroma_format_idc



# def dec_hrd_parameters(rbsp:RBSPBits):
#     hrd = {
#         'cpb_cnt_minus1':rbsp.ue(),
#         'bit_rate_scale':rbsp.u(4),
#         'cpb_rate_scale':rbsp.u(4)
#     }
#     bit_rate_value_minus1 = []
#     cpb_size_value_minus1 = []
#     cbr_flag = []
#     for SchedSelIdx in range(hrd['cpb_cnt_minus1'] + 1):
#         bit_rate_value_minus1.append(rbsp.ue())
#         cpb_size_value_minus1.append(rbsp.ue())
#         cbr_flag.append(rbsp.u(1))
#     hrd['bit_rate_value_minus1'] = bit_rate_value_minus1
#     hrd['cpb_size_value_minus1'] = cpb_size_value_minus1
#     hrd['cbr_flag'] = cbr_flag
#     hrd['inital_cpb_removal_delay_length_minus1'] = rbsp.u(5)
#     hrd['cpb_removal_delay_length_minus1'] = rbsp.u(5)
#     hrd['dpb_output_delay_length_minus1'] = rbsp.u(5)
#     hrd['time_offset_length'] = rbsp.u(5)
#     return hrd



# def dec_vui_parameters(rbsp: RBSPBits):
#     vui = {}
#     vui['aspect_ratio_info_present_flag'] = rbsp.u(1)
#     if vui['aspect_ratio_info_present_flag'] == 1:
#         vui['aspect_ratio_idc'] = rbsp.u(8)
#         if vui['aspect_ratio_idc'] == Extended_SAR :
#             vui[sar_width] = rbsp.u(16)
#             vui[sar_height] = rbsp.u(16)
#     vui['overscan_info_present_flag']=rbsp.u(1)
#     if vui['overscan_info_present_flag'] == 1:
#         vui['overscan_appropriate_flag'] = rbsp.u(1)
#     vui['video_signal_type_present_flag'] = rbsp.u(1)
#     if vui['video_signal_type_present_flag'] == 1:
#         vui['video_format'] = rbsp.u(3)
#         vui['video_full_range_flag'] = rbsp.u(1)
#         vui['colour_description_present_flag'] = rbsp.u(1)
#         if vui['colour_description_present_flag'] == 1:
#             vui['colour_primaries'] = rbsp.u(8)
#             vui['transfer_characteristics'] = rbsp.u(8)
#             vui['matix_coefficients'] = rbsp.u(8)
#     vui['chroma_loc_info_present_flag'] = rbsp.u(1)
#     if vui['chroma_loc_info_present_flag'] == 1:
#         vui['chroma_sample_loc_type_top_field'] = rbsp.ue()
#         vui['chroma_sample_loc_type_bottom_field'] = rbsp.ue()
#     vui['timing_info_present_flag'] = rbsp.u(1)
#     if vui['timing_info_present_flag'] == 1:
#         vui['num_units_in_tick'] = rbsp.u(32)
#         vui['time_scale'] = rbsp.u(32)
#         vui['fixed_frame_rate_flag'] = rbsp.u(1)
#     vui['nal_hrd_parameters_present_flag'] = rbsp.u(1)
#     if vui['nal_hrd_parameters_present_flag'] == 1:
#         vui['nal_hrd_param'] = dec_hrd_parameters(rbsp)
#     vui['vcl_hrd_parameters_present_flag'] = rbsp.u(1)
#     if vui['vcl_hrd_parameters_present_flag'] == 1:
#         vui['vcl_hrd_param'] = dec_hrd_parameters(rbsp)
#     if vui['vcl_hrd_parameters_present_flag'] or vui['nal_hrd_parameters_present_flag'] :
#         vui['low_delay_hrd_flag'] = rbsp.u(1)
    
#     vui['pic_struct_present_flag'] = rbsp.u(1)
#     vui['bitstream_restriction_flag'] = rbsp.u(1)
#     if vui['bitstream_restriction_flag'] == 1:
#         vui['montion_vectors_over_pic_boundaries_flag'] = rbsp.u(1)
#         vui['max_bytes_per_pic_denom'] = rbsp.ue()
#         vui['max_bits_per_mb_denom'] = rbsp.ue()
#         vui['log2_max_mv_length_horizontal'] = rbsp.ue()
#         vui['log2_max_mv_length_vertical'] = rbsp.ue()
#         vui['max_num_reorder_frames'] = rbsp.ue()
#         vui['max_dec_frame_buffering'] = rbsp.ue()
#     return vui
    

# def dec_seq_parameter_set_data(params, rbsp: RBSPBits):
#     sps = {
#         'profile_idc':rbsp.u(8),
#         'constraint_set0_flag':rbsp.u(1),
#         'constraint_set1_flag':rbsp.u(1),
#         'constraint_set2_flag':rbsp.u(1),
#         'constraint_set3_flag':rbsp.u(1),
#         'constraint_set4_flag':rbsp.u(1),
#         'constraint_set5_flag':rbsp.u(1),
#         'reserved_zero_2bits':rbsp.u(2),
#         'level_idc':rbsp.u(8),
#         'seq_parameter_set_id':rbsp.ue(),
#     }
#     set_default(sps)
#     profile_idc = sps['profile_idc']
#     if (profile_idc == 100 or profile_idc == 110 or 
#         profile_idc == 122 or profile_idc == 244 or 
#         profile_idc == 44  or profile_idc == 83  or 
#         profile_idc == 128 or profile_idc == 138 or 
#         profile_idc == 139 or profile_idc == 134 or profile_idc == 135):
#         sps['chroma_format_idc'] = rbsp.ue()
#         if sps['chroma_format_idc'] == 3:
#             sps['separate_colour_plane_flag'] = rbsp.u(1)
#         sps['bit_depth_luma_minus8'] = rbsp.ue()
#         sps['bit_depth_chroma_minus8'] = rbsp.ue()
#         sps['qprime_y_zero_transform_bypass_flag'] = rbsp.u(1)
#         sps['seq_scaling_matrix_present_flag'] = rbsp.u(1)
#         if sps['seq_scaling_matrix_present_flag']:
#             loop = 8 if chroma_format_idc == 3 else 12
#             list_flag = []
#             for i in range(loop):
#                 flag = rbsp.u(1)
#                 list_flag.append(flag)
#                 if flag != 0:
#                     if i < 6 :
#                         #TODO scaling_list
#                         assert False
#                     else:
#                         assert False
#             sps['seq_scaling_list_present_flag']=list_flag
                    
#     sps['log2_max_frame_num_minus4'] = rbsp.ue()
#     sps['pic_order_cnt_type'] = rbsp.ue()
#     if sps['pic_order_cnt_type'] == 0 :
#         sps['log2_max_pic_order_cnt_lsb_minus4'] = rbsp.ue()
#     elif sps['pic_order_cnt_type'] == 1:
#         sps['delta_pic_order_always_zero_flag'] = rbsp.u(1)
#         sps['offset_for_non_ref_pic'] = rbsp.se()
#         sps['offset_for_top_to_bottom_field'] = rbsp.se()
#         sps['num_ref_frames_in_pic_order_cnt_cycle'] = rbsp.ue()
#         offset_for_ref_frames = []
#         for i in range(sps['num_ref_frames_in_pic_order_cnt_cycle']):
#             offset_for_ref_frames.append(rbsp.se())

#     sps['max_num_ref_rames'] = rbsp.ue()
#     sps['gaps_in_frame_num_value_allowed_flag'] = rbsp.u(1)
#     sps['pic_width_in_mbs_minus1'] = rbsp.ue()
#     sps['pic_height_in_map_units_minus1'] = rbsp.ue()
#     sps['frame_mbs_only_flag'] = rbsp.u(1)
#     if sps['frame_mbs_only_flag'] == 0 :
#         sps['mb_adaptive_frame_filed_flag'] = rbsp.u(1)
#     sps['direct_8x8_inference_flag'] = rbsp.u(1)
#     sps['frame_cropping_flag'] = rbsp.u(1)
#     if sps['frame_cropping_flag'] == 1:
#         sps['frame_crop_left_offset'] = rbsp.ue()
#         sps['frame_crop_right_offset'] = rbsp.ue()
#         sps['frame_crop_top_offset'] = rbsp.ue()
#         sps['frame_crop_bottom_offset'] = rbsp.ue()
#     sps['vui_parameters_present_flag'] = rbsp.u(1)
#     if sps['vui_parameters_present_flag'] == 1:
#         sps['vui']=dec_vui_parameters(rbsp)
#     print(sps)
#     return sps

# def set_default(sps):
#     sps['separate_colour_plane_flag'] = 0
#     sps['mb_adaptive_frame_filed_flag'] = 0
#     sps['chroma_format_idc'] = 1
#     if sps['profile_idc'] == 183:
#         sps['chroma_format_idc'] = 0

# def PicHeightInMapUnits(sps):
#     return sps['pic_height_in_map_units_minus1'] + 1

# def FrameHeightInMbs(sps):
#     return (2 - sps['frame_mbs_only_flag']) * PicHeightInMapUnits(sps)

# def PicHeightInMbs(sps, field_pic_flag):
#     return FrameHeightInMbs(sps)//(1 + field_pic_flag)


# def PicWidthInMbs(sps):
#     return sps['pic_width_in_mbs_minus1'] + 1

# def PicWidthInSamplesL(sps):
#     return PicWidthInMbs(sps) * 16

# def PicWidthInSamplesC(sps):
#     return PicWidthInMbs(sps) * MbWidthC(sps)

# def MbWidthC(sps):
#     return 16//SubWidthC(sps)

# def MbHeightC(sps):
#     return 16//SubHeightC(sps)

# SubWidthCMap = [-1, 2, 2, 1]
# SubHeightCMap = [-1, 2, 1, 1]
# def SubWidthC(sps):
#     return SubWidthCMap[sps['chroma_format_idc']]

# def SubHeightC(sps):
#     return SubHeightCMap[sps['chroma_format_idc']]

# def PicHeightInMapUnits(sps):
#     return sps['pic_height_in_map_units_minus1'] + 1

# def PicSizeInMapUnits(sps):
#     return PicWidthInMbs(sps) * PicHeightInMapUnits(sps)

# def BitDepthY(sps):
#     return 8 + sps['bit_depth_luma_minus8']

# def QpBdOffsetY(sps):
#     return 6 * sps['bit_depth_luma_minus8']

# def BitDepthC(sps):
#     return 8 + sps['bit_depth_chroma_minus8']

# def QpBdOffsetC(sps):
#     return 6 * sps['bit_depth_chroma_minus8']

# def RawMbBits(sps):
#     return 256 * BitDepthY(sps) + 2 * MbWidthC * MbHeightC * BitDepthC