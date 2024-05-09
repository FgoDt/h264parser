from rbsp import RBSPBits

def dec_pic_parameter_set(rbsp:RBSPBits):
    pps={}
    pps['pic_parameter_set_id'] = rbsp.ue(),
    pps['seq_parameter_set_id'] = rbsp.ue(),
    pps['entropy_coding_mode_flag'] = rbsp.u(1)
    pps['pic_order_present_flag'] = rbsp.u(1)
    pps['num_slice_groups_minus1'] = rbsp.ue()
    if pps['num_slice_groups_minus1'] > 0 :
        pps['slice_group_map_type'] = rbsp.ue()
        pps['slice_group_map_top_left'] = []
        pps['slice_group_map_bottom_left'] = []
        if pps['slice_group_map_type'] == 0:
            pps['run_length_minus1'] = []
            for iGroup in range(pps['num_slice_groups_minus1'] + 1):
                pps['run_length_minus1'].append(iGroup)
        elif pps['slice_group_map_type'] == 2:
            pps['slice_group_map_top_left'].append(iGroup)
            pps['slice_group_map_bottom_left'].append(iGroup)
        elif pps['slice_group_map_type'] in [3, 5]:
            pps['slice_group_change_direction_flag'] = rbsp.u(1)
            pps['slice_group_change_rate_minus1'] = rbsp.ue()
        elif pps['slice_group_map_type'] == 6:
            pps['pic_size_in_map_units_minus1'] = rbsp.ue()
            pps['slice_group_id ']= []
            for i in range(pps['pic_size_in_map_units_minus1']+1):
                pps['slice_group_id'].append(i)
    
    pps['num_ref_idx_10_active_minus1'] = rbsp.ue()
    pps['num_ref_idx_11_active_minus1'] = rbsp.ue()
    pps['weighted_pred_flag'] = rbsp.u(1)
    pps['weighted_bipred_idc'] = rbsp.u(2)
    pps['pic_init_qp_minus26'] = rbsp.se()
    pps['pic_init_qs_minus26'] = rbsp.se()
    pps['chroma_qp_index_offset'] = rbsp.se()
    pps['deblocking_filter_control_present_flag'] = rbsp.u(1)
    pps['constrained_intra_pred_flag'] = rbsp.u(1)
    pps['redundant_pic_cnt_present_flag'] = rbsp.u(1)
    if rbsp.more_rbsp_data():
        pps['transform_8x8_mode_flag'] = rbsp.u(1)
        pps['pic_scaling_matrix_present_flag'] = rbsp.u(1)
        if pps['pic_scaling_matrix_present_flag'] == 1:
            #TODO
            assert False
        pps['second_chroma_qp_index_offset'] = rbsp.se()
    print("PPS OK")
    return pps