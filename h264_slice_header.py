from h264_pps import H264PPS
from h264_sps import H264SPS
from rbsp import RBSPBits
SLICETYPE = ['P', 'B', "I", "SP", "SI", "P", "B", "I", "SP", "SI"]
class H264SliceHeader:
    def __init__(self, param, sps:H264SPS, pps:H264PPS, rbsp:RBSPBits):
        self.forbidden_zero_bit =  param["forbidden_zero_bit"]
        self.nal_ref_idc = param["nal_ref_idc"]
        self.nal_unit_type = param["nal_unit_type"]
        self.sps = sps
        self.pps = pps
        self.rbsp = rbsp
    
    def dec(self):
        self.first_mb_in_slice = self.rbsp.ue()
        self.slice_type = self.rbsp.ue()
        slice_type = SLICETYPE[self.slice_type]
        self.slice_type = slice_type
        self.pic_parameter_set_id = self.rbsp.ue()
        if self.sps.separate_colour_plane_flag :
            self.colour_plane_id = self.rbsp.u(2)

        v = self.sps.log2_max_frame_num_minus4 + 4
        self.frame_num = self.rbsp.u(v)
        if not self.sps.frame_mbs_only_flag:
            self.field_pic_flag = self.rbsp.u(1)
            if self.field_pic_flag:
                self.bottom_field_flag = self.rbsp.u(1)
        if self.nal_unit_type == 5:
            self.idr_pic_id = self.rbsp.ue()
        if self.sps.pic_order_cnt_type == 0 :
            v = self.sps.log2_max_pic_order_cnt_lsb_minus4 + 4
            self.pic_order_cnt_lsb = self.rbsp.u(v)
            if self.pic_order_present_flag and (not self.field_pic_flag):
                self.delata_pic_order_cnt_bottom = self.rbsp.se()
        if self.pps.redundant_pic_cnt_present_flag:
            self.redundant_pic_cnt = self.rbsp.ue()
        if slice_type == "B":
            self.direct_spatial_mv_pred_flag = self.rbsp.u(1)
        if slice_type == 'P' or slice_type == 'SP' or (slice_type == 'B'):
            self.num_ref_idx_active_override_flag = self.rbsp.u(1)
            if self.num_ref_idx_active_override_flag:
                self.num_ref_idx_10_active_minus1 = self.rbsp.ue()
                if (slice_type == 'B'):
                    self.num_ref_idx_11_active_minus1 = self.rbsp.ue()
        self.ref_pic_list_reordering()
        if ((self.pps.weighted_pred_flag and ((slice_type == 'P') or (slice_type == 'SP'))) or
            ((slice_type == 'B') and self.weighted_bipred_idc)):
            self.pred_weight_table()
        if self.nal_ref_idc != 0:
            self.dec_ref_pic_marking()
        if self.pps.entropy_coding_mode_flag and ((slice_type != 'I')) and ( (slice_type != 'SI')):
            self.cbac_init_idc = self.rbsp.ue()
        self.slice_qp_delta = self.rbsp.se()
        if (slice_type == 'SP') or (slice_type == 'SI'):
            if (slice_type == 'SP'):
                self.sp_for_switch_flag = self.rbsp.u(1)
                self.slice_qs_delta = self.rbsp.se()
        if self.pps.deblocking_filter_control_present_flag:
            self.disable_deblocking_filter_idc = self.rbsp.ue()
            if self.disable_deblocking_filter_idc != 1:
                self.slice_alpha_c0_offset_div2 = self.rbsp.se()
                self.slice_beta_offset_div2 = self.rbsp.se()
        if self.pps.num_slice_groups_minus1 > 0 and self.slice_group_map_type >= 3 and self.slice_group_map_type <= 5:
            v = math.ceil(math.log2(h264sps.PicSizeInMapUnits(sps)//h264pps.SliceGroupChangeRate(pps) + 1))
            self.slice_group_change_cycle = self.rbsp.u(v)

        print(self)
    
    def ref_pic_list_reordering(self):
        slice_type = self.slice_type
        if ((slice_type != 'I')) and ((slice_type !='SI')):
            self.ref_pic_list_reordering_flag_10 = self.rbsp.u(1)
            if self.ref_pic_list_reordering_flag_10 :
                while True:
                    idc = self.rbsp.ue()
                    self.reordering_of_pic_nums_idc = idc
                    if idc == 0 or idc == 1:
                        self.abs_diff_pic_num_minus1 = self.rbsp.ue()
                    elif idc == 2:
                        self.long_term_pic_num = self.rbsp.ue()

                    if idc == 3:
                        break
        if (slice_type == 'B'):
            self.ref_pic_list_reordering_flag_11 = self.rbsp.u(1)
            if self.ref_pic_list_reordering_flag_11:
               while True:
                    idc = self.rbsp.ue()
                    self.reordering_of_pic_nums_idc = idc
                    if idc == 0 or idc == 1:
                        self.abs_diff_pic_num_minus1 = self.rbsp.ue()
                    elif idc == 2:
                        self.long_term_pic_num = self.rbsp.ue()

                    if idc == 3:
                        break 

    def pred_weight_table(self):
        self.luma_log2_weight_denom = self.rbsp.ue()
        if self.sps.chroma_format_idc != 0 :
            self.chroma_log2_weight_denom = self.rbsp.ue()
        assert False
        pass

    def dec_ref_pic_marking(self):
        if self.nal_unit_type == 5 :
            self.no_output_of_prior_pics_flag = self.rbsp.u(1)
            self.long_term_reference_flag = self.rbsp.u(1)
        else:
            self.adaptive_ref_pic_marking_mode_flag = self.rbsp.u(1)
            if self.adaptive_ref_pic_marking_mode_flag:
                while True:
                    operation = self.rbsp.ue()
                    self.memory_management_control_operation = operation
                    if operation == 1 or operation == 3:
                        self.difference_of_pic_nums_minus1 = self.rbsp.ue()
                    if operation == 2:
                        self.long_term_pic_num = self.rbsp.ue()
                    if operation == 3 or operation == 6:
                        self.long_term_frame_idx = self.rbsp.ue()
                    if operation == 4:
                        self.max_long_term_frame_idx_plus1 = self.rbsp.ue()
                    if operation == 0:
                        break