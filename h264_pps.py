from rbsp import RBSPBits

class H264PPS:
    def __init__(self, rbsp:RBSPBits):
        self.rbsp = rbsp
        self.transform_8x8_mode_flag = 0
        self.slice_group_change_rate_minus1 = 0
    
    def dec(self):
        self.pic_parameter_set_id = self.rbsp.ue(),
        self.seq_parameter_set_id = self.rbsp.ue(),
        self.entropy_coding_mode_flag = self.rbsp.u(1)
        self.pic_order_present_flag = self.rbsp.u(1)
        self.num_slice_groups_minus1 = self.rbsp.ue()
        
        if self.num_slice_groups_minus1 > 0:
            self.slice_group_map_type = self.rbsp.ue()
            self.slice_group_map_top_left = []
            self.slice_group_map_bottom_left = []
            if self.slice_group_map_type == 0:
                self.run_length_minus1 = []
                for iGroup in range(self.num_slice_groups_minus1 + 1):
                    self.run_length_minus1.append(iGroup)
            elif self.slice_group_map_type == 2:
                self.slice_group_map_top_left.append(iGroup)
                self.slice_group_map_bottom_left.append(iGroup)
            elif self.slice_group_map_type in [3, 5]:
                self.slice_group_change_direction_flag = self.rbsp.u(1)
                self.slice_group_change_rate_minus1 = self.rbsp.ue()
            elif self.slice_group_map_type == 6:
                self.pic_size_in_map_units_minus1 = self.rbsp.ue()
                self.slice_group_id = []
                for i in range(self.pic_size_in_map_units_minus1+1):
                    self.slice_group_id.append(i)
        
        self.num_ref_idx_10_active_minus1 = self.rbsp.ue()
        self.num_ref_idx_11_active_minus1 = self.rbsp.ue()
        self.weighted_pred_flag = self.rbsp.u(1)
        self.weighted_bipred_idc = self.rbsp.u(2)
        self.pic_init_qp_minus26 = self.rbsp.se()
        self.pic_init_qs_minus26 = self.rbsp.se()
        self.chroma_qp_index_offset = self.rbsp.se()
        self.deblocking_filter_control_present_flag = self.rbsp.u(1)
        self.constrained_intra_pred_flag = self.rbsp.u(1)
        self.redundant_pic_cnt_present_flag = self.rbsp.u(1)
        if self.rbsp.more_rbsp_data():
            self.transform_8x8_mode_flag = self.rbsp.u(1)
            self.pic_scaling_matrix_present_flag = self.rbsp.u(1)
            if self.pic_scaling_matrix_present_flag == 1:
                #TODO
                assert False
            self.second_chroma_qp_index_offset = self.rbsp.se()
        
        self.cal_val()
        print("PPS OK")
    
    def cal_val(self):
        self.SliceGroupChangeRate = self.slice_group_change_rate_minus1 + 1

# def dec_pic_parameter_set(rbsp:RBSPBits):
#     pps={}
#     set_default(pps)
#     pps['pic_parameter_set_id'] = rbsp.ue(),
#     pps['seq_parameter_set_id'] = rbsp.ue(),
#     pps['entropy_coding_mode_flag'] = rbsp.u(1)
#     pps['pic_order_present_flag'] = rbsp.u(1)
#     pps['num_slice_groups_minus1'] = rbsp.ue()
#     if pps['num_slice_groups_minus1'] > 0 :
#         pps['slice_group_map_type'] = rbsp.ue()
#         pps['slice_group_map_top_left'] = []
#         pps['slice_group_map_bottom_left'] = []
#         if pps['slice_group_map_type'] == 0:
#             pps['run_length_minus1'] = []
#             for iGroup in range(pps['num_slice_groups_minus1'] + 1):
#                 pps['run_length_minus1'].append(iGroup)
#         elif pps['slice_group_map_type'] == 2:
#             pps['slice_group_map_top_left'].append(iGroup)
#             pps['slice_group_map_bottom_left'].append(iGroup)
#         elif pps['slice_group_map_type'] in [3, 5]:
#             pps['slice_group_change_direction_flag'] = rbsp.u(1)
#             pps['slice_group_change_rate_minus1'] = rbsp.ue()
#         elif pps['slice_group_map_type'] == 6:
#             pps['pic_size_in_map_units_minus1'] = rbsp.ue()
#             pps['slice_group_id ']= []
#             for i in range(pps['pic_size_in_map_units_minus1']+1):
#                 pps['slice_group_id'].append(i)
    
#     pps['num_ref_idx_10_active_minus1'] = rbsp.ue()
#     pps['num_ref_idx_11_active_minus1'] = rbsp.ue()
#     pps['weighted_pred_flag'] = rbsp.u(1)
#     pps['weighted_bipred_idc'] = rbsp.u(2)
#     pps['pic_init_qp_minus26'] = rbsp.se()
#     pps['pic_init_qs_minus26'] = rbsp.se()
#     pps['chroma_qp_index_offset'] = rbsp.se()
#     pps['deblocking_filter_control_present_flag'] = rbsp.u(1)
#     pps['constrained_intra_pred_flag'] = rbsp.u(1)
#     pps['redundant_pic_cnt_present_flag'] = rbsp.u(1)
#     if rbsp.more_rbsp_data():
#         pps['transform_8x8_mode_flag'] = rbsp.u(1)
#         pps['pic_scaling_matrix_present_flag'] = rbsp.u(1)
#         if pps['pic_scaling_matrix_present_flag'] == 1:
#             #TODO
#             assert False
#         pps['second_chroma_qp_index_offset'] = rbsp.se()
#     print("PPS OK")
#     return pps

# def set_default(pps):
#     pps['transform_8x8_mode_flag'] = 0


# def SliceGroupChangeRate(pps):
#     return pps['slice_group_change_rate_minus1'] + 1