from rbsp import RBSPBits
import math
import h264pps
import h264sps

SLICETYPE = ['P', 'B', "I", "SP", "SI", "P", "B", "I", "SP", "SI"]


def slice_layer_without_partitioning_rbsp(param, sps, pps, rbsp:RBSPBits):
    header = slice_header(param, sps, pps, rbsp)
    slice_data(header, param, sps, pps, rbsp)
    pass

def slice_header(param, sps, pps, rbsp:RBSPBits):
    header = {}
    header['first_mb_in_slice'] = rbsp.ue()
    header['slice_type'] = rbsp.ue()
    slice_type = SLICETYPE[header['slice_type']]
    header['pic_parameter_set_id'] = rbsp.ue()
    if sps['separate_colour_plane_flag'] :
        header['colour_plane_id'] = rbsp.u(2)

    v = sps['log2_max_frame_num_minus4'] + 4
    header['frame_num'] = rbsp.u(v)
    if not sps['frame_mbs_only_flag']:
        header['field_pic_flag'] = rbsp.u(1)
        if header['field_pic_flag']:
            header['bottom_field_flag'] = rbsp.u(1)
    if param['nal_unit_type'] == 5:
        header['idr_pic_id'] = rbsp.ue()
    if sps['pic_order_cnt_type'] == 0 :
        v = sps['log2_max_pic_order_cnt_lsb_minus4'] + 4
        header['pic_order_cnt_lsb'] = rbsp.u(v)
        if pps['pic_order_present_flag'] and (not header['field_pic_flag']):
            header['delata_pic_order_cnt_bottom'] = rbsp.se()
    if pps["redundant_pic_cnt_present_flag"]:
        header['redundant_pic_cnt'] = rbsp.ue()
    if slice_type == "B":
        header['direct_spatial_mv_pred_flag'] = rbsp.u(1)
    if slice_type == 'P' or slice_type == 'SP' or (slice_type == 'B'):
        header['num_ref_idx_active_override_flag'] = rbsp.u(1)
        if header['num_ref_idx_active_override_flag']:
            header['num_ref_idx_10_active_minus1'] = rbsp.ue()
            if (slice_type == 'B'):
                header['num_ref_idx_11_active_minus1'] = rbsp.ue()
    ref_pic_list_reordering(header, sps, pps, rbsp)
    if ((pps['weighted_pred_flag'] and ((slice_type == 'P') or (slice_type == 'SP'))) or
        ((slice_type == 'B') and pps['weighted_bipred_idc'])):
        pred_weight_table()
    if param['nal_ref_idc'] != 0:
        dec_ref_pic_marking(header, param, sps, pps, rbsp)
    if pps['entropy_coding_mode_flag'] and ((slice_type != 'I')) and ( (slice_type != 'SI')):
        header['cbac_init_idc'] = rbsp.ue()
    header['slice_qp_delta'] = rbsp.se()
    if (slice_type == 'SP') or (slice_type == 'SI'):
        if (slice_type == 'SP'):
            header['sp_for_switch_flag'] = rbsp.u(1)
            header['slice_qs_delta'] = rbsp.se()
    if pps['deblocking_filter_control_present_flag']:
        header['disable_deblocking_filter_idc'] = rbsp.ue()
        if header['disable_deblocking_filter_idc'] != 1:
            header['slice_alpha_c0_offset_div2'] = rbsp.se()
            header['slice_beta_offset_div2'] = rbsp.se()
    if pps['num_slice_groups_minus1'] > 0 and pps['slice_group_map_type'] >= 3 and pps['slice_group_map_type'] <= 5:
        v = math.ceil(math.log2(h264sps.PicSizeInMapUnits(sps)//h264pps.SliceGroupChangeRate(pps) + 1))
        header['slice_group_change_cycle'] = rbsp.u(v)
    return header

def slice_data(header, param, sps, pps, rbsp:RBSPBits):
    if pps['entropy_coding_mode_flag']:
        while not rbsp.byte_aligned():
            rbsp.f(1)
    slice_type = SLICETYPE[header['slice_type']]
    MbaffFrameFlag = 1 if sps['mb_adaptive_frame_filed_flag'] and header['field_pic_flag'] else 0
    CurrMbAddr = header['first_mb_in_slice'] * ( 1 + MbaffFrameFlag)
    moreDataFlag = True
    prevMbSkipped = False

    data = {}

    while True:
        if slice_type != 'I' and slice_type != 'SI':
            if not pps['entropy_coding_mode_flag']:
                data['mb_skip_run'] = rbsp.ue()
                prevMbSkipped = True if data['mb_skip_run'] > 0 else False
                for i in range(data['mb_skip_run']):
                    CurrMbAddr = NextMbAddress(CurrMbAddr)
                moreDataFlag = rbsp.more_rbsp_data()
            else:
                data['mb_skip_flag'] = rbsp.ae()
                moreDataFlag = not data['mb_skip_flag']
        break
    return data



def ref_pic_list_reordering(header, sps, pps, rbsp:RBSPBits):
    slice_type = SLICETYPE[header['slice_type']]
    if ((slice_type != 'I')) and ((slice_type !='SI')):
        header['ref_pic_list_reordering_flag_10'] = rbsp.u(1)
        if header['ref_pic_list_reordering_flag_10'] :
            while True:
                idc = rbsp.ue()
                header['reordering_of_pic_nums_idc'] = idc
                if idc == 0 or idc == 1:
                    header['abs_diff_pic_num_minus1'] = rbsp.ue()
                elif idc == 2:
                    header['long_term_pic_num'] = rbsp.ue()
                
                if idc == 3:
                    break
    if (slice_type == 'B'):
        header['ref_pic_list_reordering_flag_11'] = rbsp.u(1)
        if header['ref_pic_list_reordering_flag_11']:
           while True:
                idc = rbsp.ue()
                header['reordering_of_pic_nums_idc'] = idc
                if idc == 0 or idc == 1:
                    header['abs_diff_pic_num_minus1'] = rbsp.ue()
                elif idc == 2:
                    header['long_term_pic_num'] = rbsp.ue()
                
                if idc == 3:
                    break 
    pass

def pred_weight_table(header, param, sps, pps, rbsp:RBSPBits):
    header['luma_log2_weight_denom'] = rbsp.ue()
    if sps['chroma_format_idc'] != 0 :
        header['chroma_log2_weight_denom'] = rbsp.ue()
    assert False
    pass

def dec_ref_pic_marking(header, param, sps, pps, rbsp):
    if param['nal_unit_type'] == 5 :
        header['no_output_of_prior_pics_flag'] = rbsp.u(1)
        header['long_term_reference_flag'] = rbsp.u(1)
    else:
        header['adaptive_ref_pic_marking_mode_flag'] = rbsp.u(1)
        if header['adaptive_ref_pic_marking_mode_flag']:
            while True:
                operation = rbsp.ue()
                header['memory_management_control_operation'] = operation
                if operation == 1 or operation == 3:
                    header['difference_of_pic_nums_minus1'] = rbsp.ue()
                if operation == 2:
                    header['long_term_pic_num'] = rbsp.ue()
                if operation == 3 or operation == 6:
                    header['long_term_frame_idx'] = rbsp.ue()
                if operation == 4:
                    header['max_long_term_frame_idx_plus1'] = rbsp.ue()
                if operation == 0:
                    break
