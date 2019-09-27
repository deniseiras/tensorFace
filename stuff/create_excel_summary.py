import csv
import os

def calc_mean(arr2, idx):
    if len(arr2) == 0:
        return  0.0
    summ = calc_sum(arr2, idx)
    return summ / len(arr2)


def calc_sum(arr2, idx):
    summ = 0
    for arr_each in arr2:
        summ += float(arr_each[idx])
    return summ


dir_exp = '/media/denis/dados/dev/tensorface_data/experiments/'
dir_saidas = '/mnt/cloud/Dropbox/__msc/Dissertação/figuras/saidas/'
filenamez = []


# YUV mean
# base = 'yuv_mean'
# filenamez.append('Unitau_info_2_1a_sessao_sem_2_a_4_yuv_iluminance_mean_0.1/log/Unitau_info_2_1a_sessao_sem_2_a_4_224_1.0_5000_none_yuv_iluminance_mean_0.1__20190123-164716_summary.csv')
# filenamez.append('Unitau_info_2_1a_sessao_sem_2_a_4_yuv_iluminance_mean_0.2/log/Unitau_info_2_1a_sessao_sem_2_a_4_224_1.0_5000_none_yuv_iluminance_mean_0.2__20190123-172456_summary.csv')
# filenamez.append('Unitau_info_2_1a_sessao_sem_2_a_4_yuv_iluminance_mean_0.3/log/Unitau_info_2_1a_sessao_sem_2_a_4_224_1.0_5000_none_yuv_iluminance_mean_0.3__20190123-180237_summary.csv')
# filenamez.append('Unitau_info_2_1a_sessao_sem_2_a_4_yuv_iluminance_mean_0.4/log/Unitau_info_2_1a_sessao_sem_2_a_4_224_1.0_5000_none_yuv_iluminance_mean_0.4__20190123-183936_summary.csv')
# filenamez.append('Unitau_info_2_1a_sessao_sem_2_a_4_yuv_iluminance_mean_0.5/log/Unitau_info_2_1a_sessao_sem_2_a_4_224_1.0_5000_none_yuv_iluminance_mean_0.5__20190123-191857_summary.csv')
# filenamez.append('Unitau_info_2_1a_sessao_sem_2_a_4_yuv_iluminance_mean_0.6/log/Unitau_info_2_1a_sessao_sem_2_a_4_224_1.0_5000_none_yuv_iluminance_mean_0.6__20190123-195736_summary.csv')
# filenamez.append('Unitau_info_2_1a_sessao_sem_2_a_4_yuv_iluminance_mean_0.7/log/Unitau_info_2_1a_sessao_sem_2_a_4_224_1.0_5000_none_yuv_iluminance_mean_0.7__20190123-203543_summary.csv')
# filenamez.append('Unitau_info_2_1a_sessao_sem_2_a_4_yuv_iluminance_mean_0.8/log/Unitau_info_2_1a_sessao_sem_2_a_4_224_1.0_5000_none_yuv_iluminance_mean_0.8__20190123-211350_summary.csv')
# filenamez.append('Unitau_info_2_1a_sessao_sem_2_a_4_yuv_iluminance_mean_0.9/log/Unitau_info_2_1a_sessao_sem_2_a_4_224_1.0_5000_none_yuv_iluminance_mean_0.9__20190123-214920_summary.csv')
# filenamez.append('Unitau_info_2_1a_sessao_sem_2_a_4_yuv_iluminance_mean_1.0/log/Unitau_info_2_1a_sessao_sem_2_a_4_224_1.0_5000_none_yuv_iluminance_mean_1.0__20190124-131113_summary.csv')


# YUV median
# base = 'yuv_median'
# filenamez.append('Unitau_info_2_1a_sessao_sem_2_a_4_yuv_iluminance_median_0.1/log/Unitau_info_2_1a_sessao_sem_2_a_4_224_1.0_5000_none_yuv_iluminance_median_0.1__20190123-215028_summary.csv')
# filenamez.append('Unitau_info_2_1a_sessao_sem_2_a_4_yuv_iluminance_median_0.2/log/Unitau_info_2_1a_sessao_sem_2_a_4_224_1.0_5000_none_yuv_iluminance_median_0.2__20190123-223342_summary.csv')
# filenamez.append('Unitau_info_2_1a_sessao_sem_2_a_4_yuv_iluminance_median_0.3/log/Unitau_info_2_1a_sessao_sem_2_a_4_224_1.0_5000_none_yuv_iluminance_median_0.3__20190123-230100_summary.csv')
# filenamez.append('Unitau_info_2_1a_sessao_sem_2_a_4_yuv_iluminance_median_0.4/log/Unitau_info_2_1a_sessao_sem_2_a_4_224_1.0_5000_none_yuv_iluminance_median_0.4__20190123-232831_summary.csv')
# filenamez.append('Unitau_info_2_1a_sessao_sem_2_a_4_yuv_iluminance_median_0.5/log/Unitau_info_2_1a_sessao_sem_2_a_4_224_1.0_5000_none_yuv_iluminance_median_0.5__20190124-005536_summary.csv')
# filenamez.append('Unitau_info_2_1a_sessao_sem_2_a_4_yuv_iluminance_median_0.6/log/Unitau_info_2_1a_sessao_sem_2_a_4_224_1.0_5000_none_yuv_iluminance_median_0.6__20190124-012234_summary.csv')
# filenamez.append('Unitau_info_2_1a_sessao_sem_2_a_4_yuv_iluminance_median_0.7/log/Unitau_info_2_1a_sessao_sem_2_a_4_224_1.0_5000_none_yuv_iluminance_median_0.7__20190124-112737_summary.csv')
# filenamez.append('Unitau_info_2_1a_sessao_sem_2_a_4_yuv_iluminance_median_0.8/log/Unitau_info_2_1a_sessao_sem_2_a_4_224_1.0_5000_none_yuv_iluminance_median_0.8__20190124-115442_summary.csv')
# filenamez.append('Unitau_info_2_1a_sessao_sem_2_a_4_yuv_iluminance_median_0.9/log/Unitau_info_2_1a_sessao_sem_2_a_4_224_1.0_5000_none_yuv_iluminance_median_0.9__20190124-123220_summary.csv')
# filenamez.append('Unitau_info_2_1a_sessao_sem_2_a_4_yuv_iluminance_median_1.0/log/Unitau_info_2_1a_sessao_sem_2_a_4_224_1.0_5000_none_yuv_iluminance_median_1.0__20190124-153331_summary.csv')

# =========================================
# # Y var
base = 'y_var'
filenamez.append('Unitau_info_2_sessao_2_a_4_y_variance_0.1/log/Unitau_info_2_sessao_2_a_4_224_1.0_5000_none_y_variance_0.1_summary.csv')
filenamez.append('Unitau_info_2_sessao_2_a_4_y_variance_0.2/log/Unitau_info_2_sessao_2_a_4_224_1.0_5000_none_y_variance_0.2_summary.csv')
filenamez.append('Unitau_info_2_sessao_2_a_4_y_variance_0.3/log/Unitau_info_2_sessao_2_a_4_224_1.0_5000_none_y_variance_0.3_summary.csv')
filenamez.append('Unitau_info_2_sessao_2_a_4_y_variance_0.4/log/Unitau_info_2_sessao_2_a_4_224_1.0_5000_none_y_variance_0.4_summary.csv')
filenamez.append('Unitau_info_2_sessao_2_a_4_y_variance_0.5/log/Unitau_info_2_sessao_2_a_4_224_1.0_5000_none_y_variance_0.5_summary.csv')
filenamez.append('Unitau_info_2_sessao_2_a_4_y_variance_0.6/log/Unitau_info_2_sessao_2_a_4_224_1.0_5000_none_y_variance_0.6_summary.csv')
filenamez.append('Unitau_info_2_sessao_2_a_4_y_variance_0.7/log/Unitau_info_2_sessao_2_a_4_224_1.0_5000_none_y_variance_0.7_summary.csv')
filenamez.append('Unitau_info_2_sessao_2_a_4_y_variance_0.8/log/Unitau_info_2_sessao_2_a_4_224_1.0_5000_none_y_variance_0.8_summary.csv')
filenamez.append('Unitau_info_2_sessao_2_a_4_y_variance_0.9/log/Unitau_info_2_sessao_2_a_4_224_1.0_5000_none_y_variance_0.9_summary.csv')
filenamez.append('Unitau_info_2_sessao_2_a_4_y_variance_1.0/log/Unitau_info_2_sessao_2_a_4_224_1.0_5000_none_y_variance_1.0_summary.csv')

# # Y mean
# base = 'y_mean'
# filenamez.append('Unitau_info_2_sessao_2_a_4_y_mean_0.1/log/Unitau_info_2_sessao_2_a_4_224_1.0_5000_none_y_mean_0.1_summary.csv')
# filenamez.append('Unitau_info_2_sessao_2_a_4_y_mean_0.2/log/Unitau_info_2_sessao_2_a_4_224_1.0_5000_none_y_mean_0.2_summary.csv')
# filenamez.append('Unitau_info_2_sessao_2_a_4_y_mean_0.3/log/Unitau_info_2_sessao_2_a_4_224_1.0_5000_none_y_mean_0.3_summary.csv')
# filenamez.append('Unitau_info_2_sessao_2_a_4_y_mean_0.4/log/Unitau_info_2_sessao_2_a_4_224_1.0_5000_none_y_mean_0.4_summary.csv')
# filenamez.append('Unitau_info_2_sessao_2_a_4_y_mean_0.5/log/Unitau_info_2_sessao_2_a_4_224_1.0_5000_none_y_mean_0.5_summary.csv')
# filenamez.append('Unitau_info_2_sessao_2_a_4_y_mean_0.6/log/Unitau_info_2_sessao_2_a_4_224_1.0_5000_none_y_mean_0.6_summary.csv')
# filenamez.append('Unitau_info_2_sessao_2_a_4_y_mean_0.7/log/Unitau_info_2_sessao_2_a_4_224_1.0_5000_none_y_mean_0.7_summary.csv')
# filenamez.append('Unitau_info_2_sessao_2_a_4_y_mean_0.8/log/Unitau_info_2_sessao_2_a_4_224_1.0_5000_none_y_mean_0.8_summary.csv')
# filenamez.append('Unitau_info_2_sessao_2_a_4_y_mean_0.9/log/Unitau_info_2_sessao_2_a_4_224_1.0_5000_none_y_mean_0.9_summary.csv')
# filenamez.append('Unitau_info_2_sessao_2_a_4_y_mean_1.0/log/Unitau_info_2_sessao_2_a_4_224_1.0_5000_none_y_mean_1.0_summary.csv')

# Y median
# base = 'y_median'
# filenamez.append('Unitau_info_2_sessao_2_a_4_y_median_0.1/log/Unitau_info_2_sessao_2_a_4_224_1.0_5000_none_y_median_0.1_summary.csv')
# filenamez.append('Unitau_info_2_sessao_2_a_4_y_median_0.2/log/Unitau_info_2_sessao_2_a_4_224_1.0_5000_none_y_median_0.2_summary.csv')
# filenamez.append('Unitau_info_2_sessao_2_a_4_y_median_0.3/log/Unitau_info_2_sessao_2_a_4_224_1.0_5000_none_y_median_0.3_summary.csv')
# filenamez.append('Unitau_info_2_sessao_2_a_4_y_median_0.4/log/Unitau_info_2_sessao_2_a_4_224_1.0_5000_none_y_median_0.4_summary.csv')
# filenamez.append('Unitau_info_2_sessao_2_a_4_y_median_0.5/log/Unitau_info_2_sessao_2_a_4_224_1.0_5000_none_y_median_0.5_summary.csv')
# filenamez.append('Unitau_info_2_sessao_2_a_4_y_median_0.6/log/Unitau_info_2_sessao_2_a_4_224_1.0_5000_none_y_median_0.6_summary.csv')
# filenamez.append('Unitau_info_2_sessao_2_a_4_y_median_0.7/log/Unitau_info_2_sessao_2_a_4_224_1.0_5000_none_y_median_0.7_summary.csv')
# filenamez.append('Unitau_info_2_sessao_2_a_4_y_median_0.8/log/Unitau_info_2_sessao_2_a_4_224_1.0_5000_none_y_median_0.8_summary.csv')
# filenamez.append('Unitau_info_2_sessao_2_a_4_y_median_0.9/log/Unitau_info_2_sessao_2_a_4_224_1.0_5000_none_y_median_0.9_summary.csv')
# filenamez.append('Unitau_info_2_sessao_2_a_4_y_median_1.0/log/Unitau_info_2_sessao_2_a_4_224_1.0_5000_none_y_median_1.0_summary.csv')

# Y STD
# base = 'y_std'
# filenamez.append('Unitau_info_2_sessao_2_a_4_y_std_0.1/log/Unitau_info_2_sessao_2_a_4_224_1.0_5000_none_y_std_0.1_summary.csv')
# filenamez.append('Unitau_info_2_sessao_2_a_4_y_std_0.2/log/Unitau_info_2_sessao_2_a_4_224_1.0_5000_none_y_std_0.2_summary.csv')
# filenamez.append('Unitau_info_2_sessao_2_a_4_y_std_0.3/log/Unitau_info_2_sessao_2_a_4_224_1.0_5000_none_y_std_0.3_summary.csv')
# filenamez.append('Unitau_info_2_sessao_2_a_4_y_std_0.4/log/Unitau_info_2_sessao_2_a_4_224_1.0_5000_none_y_std_0.4_summary.csv')
# filenamez.append('Unitau_info_2_sessao_2_a_4_y_std_0.5/log/Unitau_info_2_sessao_2_a_4_224_1.0_5000_none_y_std_0.5_summary.csv')
# filenamez.append('Unitau_info_2_sessao_2_a_4_y_std_0.6/log/Unitau_info_2_sessao_2_a_4_224_1.0_5000_none_y_std_0.6_summary.csv')
# filenamez.append('Unitau_info_2_sessao_2_a_4_y_std_0.7/log/Unitau_info_2_sessao_2_a_4_224_1.0_5000_none_y_std_0.7_summary.csv')
# filenamez.append('Unitau_info_2_sessao_2_a_4_y_std_0.8/log/Unitau_info_2_sessao_2_a_4_224_1.0_5000_none_y_std_0.8_summary.csv')
# filenamez.append('Unitau_info_2_sessao_2_a_4_y_std_0.9/log/Unitau_info_2_sessao_2_a_4_224_1.0_5000_none_y_std_0.9_summary.csv')
# filenamez.append('Unitau_info_2_sessao_2_a_4_y_std_1.0/log/Unitau_info_2_sessao_2_a_4_224_1.0_5000_none_y_std_1.0_summary.csv')


# HISTOGRAM =========================================
# Y shadow
# base = 'y_shadow_factor'
# filenamez.append('Unitau_info_2 sessao_2_a_4_y_shadow_factor_0.1/log/Unitau_info_2 sessao_2_a_4_224_1.0_5000_none_y_shadow_factor_0.1__20190131-193519_summary.csv')
# filenamez.append('Unitau_info_2 sessao_2_a_4_y_shadow_factor_0.2/log/Unitau_info_2 sessao_2_a_4_224_1.0_5000_none_y_shadow_factor_0.2__20190131-195923_summary.csv')
# filenamez.append('Unitau_info_2 sessao_2_a_4_y_shadow_factor_0.3/log/Unitau_info_2 sessao_2_a_4_224_1.0_5000_none_y_shadow_factor_0.3__20190131-202703_summary.csv')
# filenamez.append('Unitau_info_2 sessao_2_a_4_y_shadow_factor_0.4/log/Unitau_info_2 sessao_2_a_4_224_1.0_5000_none_y_shadow_factor_0.4__20190131-205537_summary.csv')
# filenamez.append('Unitau_info_2 sessao_2_a_4_y_shadow_factor_0.5/log/Unitau_info_2 sessao_2_a_4_224_1.0_5000_none_y_shadow_factor_0.5__20190131-233652_summary.csv')
# filenamez.append('Unitau_info_2 sessao_2_a_4_y_shadow_factor_0.6/log/Unitau_info_2 sessao_2_a_4_224_1.0_5000_none_y_shadow_factor_0.6__20190201-083757_summary.csv')
# filenamez.append('Unitau_info_2 sessao_2_a_4_y_shadow_factor_0.7/log/Unitau_info_2 sessao_2_a_4_224_1.0_5000_none_y_shadow_factor_0.7__20190201-091038_summary.csv')
# filenamez.append('Unitau_info_2 sessao_2_a_4_y_shadow_factor_0.8/log/Unitau_info_2 sessao_2_a_4_224_1.0_5000_none_y_shadow_factor_0.8__20190201-094501_summary.csv')
# filenamez.append('Unitau_info_2 sessao_2_a_4_y_shadow_factor_0.9/log/Unitau_info_2 sessao_2_a_4_224_1.0_5000_none_y_shadow_factor_0.9__20190201-101957_summary.csv')
# filenamez.append('Unitau_info_2 sessao_2_a_4_y_shadow_factor_1.0/log/Unitau_info_2 sessao_2_a_4_224_1.0_5000_none_y_shadow_factor_1.0__20190201-105642_summary.csv')

# base = 'y_highlight_factor'
# filenamez.append('Unitau_info_2 sessao_2_a_4_y_highlight_factor_0.1/log/Unitau_info_2 sessao_2_a_4_224_1.0_5000_none_y_highlight_factor_0.1__20190131-192513_summary.csv')
# filenamez.append('Unitau_info_2 sessao_2_a_4_y_highlight_factor_0.2/log/Unitau_info_2 sessao_2_a_4_224_1.0_5000_none_y_highlight_factor_0.2__20190131-194813_summary.csv')
# filenamez.append('Unitau_info_2 sessao_2_a_4_y_highlight_factor_0.3/log/Unitau_info_2 sessao_2_a_4_224_1.0_5000_none_y_highlight_factor_0.3__20190131-201503_summary.csv')
# filenamez.append('Unitau_info_2 sessao_2_a_4_y_highlight_factor_0.4/log/Unitau_info_2 sessao_2_a_4_224_1.0_5000_none_y_highlight_factor_0.4__20190131-204323_summary.csv')
# filenamez.append('Unitau_info_2 sessao_2_a_4_y_highlight_factor_0.5/log/Unitau_info_2 sessao_2_a_4_224_1.0_5000_none_y_highlight_factor_0.5__20190131-232102_summary.csv')
# filenamez.append('Unitau_info_2 sessao_2_a_4_y_highlight_factor_0.6/log/Unitau_info_2 sessao_2_a_4_224_1.0_5000_none_y_highlight_factor_0.6__20190201-082424_summary.csv')
# filenamez.append('Unitau_info_2 sessao_2_a_4_y_highlight_factor_0.7/log/Unitau_info_2 sessao_2_a_4_224_1.0_5000_none_y_highlight_factor_0.7__20190201-085539_summary.csv')
# filenamez.append('Unitau_info_2 sessao_2_a_4_y_highlight_factor_0.8/log/Unitau_info_2 sessao_2_a_4_224_1.0_5000_none_y_highlight_factor_0.8__20190201-092852_summary.csv')
# filenamez.append('Unitau_info_2 sessao_2_a_4_y_highlight_factor_0.9/log/Unitau_info_2 sessao_2_a_4_224_1.0_5000_none_y_highlight_factor_0.9__20190201-100327_summary.csv')
# filenamez.append('Unitau_info_2 sessao_2_a_4_y_highlight_factor_1.0/log/Unitau_info_2 sessao_2_a_4_224_1.0_5000_none_y_highlight_factor_1.0__20190201-103825_summary.csv')

# Y medium hist mean\
# base = 'y_medium_hist_mean'
# filenamez.append('Unitau_info_2_1a_sessao_sem_2_a_4_y_medium_hist_mean_0.1/log/Unitau_info_2_1a_sessao_sem_2_a_4_224_1.0_5000_none_y_medium_hist_mean_0.1__20190128-184914_summary.csv')
# filenamez.append('Unitau_info_2_1a_sessao_sem_2_a_4_y_medium_hist_mean_0.2/log/Unitau_info_2_1a_sessao_sem_2_a_4_224_1.0_5000_none_y_medium_hist_mean_0.2__20190128-192358_summary.csv')
# filenamez.append('Unitau_info_2_1a_sessao_sem_2_a_4_y_medium_hist_mean_0.3/log/Unitau_info_2_1a_sessao_sem_2_a_4_224_1.0_5000_none_y_medium_hist_mean_0.3__20190128-195743_summary.csv')
# filenamez.append('Unitau_info_2_1a_sessao_sem_2_a_4_y_medium_hist_mean_0.4/log/Unitau_info_2_1a_sessao_sem_2_a_4_224_1.0_5000_none_y_medium_hist_mean_0.4__20190128-203304_summary.csv')
# filenamez.append('Unitau_info_2_1a_sessao_sem_2_a_4_y_medium_hist_mean_0.5/log/Unitau_info_2_1a_sessao_sem_2_a_4_224_1.0_5000_none_y_medium_hist_mean_0.5__20190128-210857_summary.csv')
# filenamez.append('Unitau_info_2_1a_sessao_sem_2_a_4_y_medium_hist_mean_0.6/log/Unitau_info_2_1a_sessao_sem_2_a_4_224_1.0_5000_none_y_medium_hist_mean_0.6__20190128-214511_summary.csv')
# filenamez.append('Unitau_info_2_1a_sessao_sem_2_a_4_y_medium_hist_mean_0.7/log/Unitau_info_2_1a_sessao_sem_2_a_4_224_1.0_5000_none_y_medium_hist_mean_0.7__20190128-222153_summary.csv')
# filenamez.append('Unitau_info_2_1a_sessao_sem_2_a_4_y_medium_hist_mean_0.8/log/Unitau_info_2_1a_sessao_sem_2_a_4_224_1.0_5000_none_y_medium_hist_mean_0.8__20190128-225833_summary.csv')
# filenamez.append('Unitau_info_2_1a_sessao_sem_2_a_4_y_medium_hist_mean_0.9/log/Unitau_info_2_1a_sessao_sem_2_a_4_224_1.0_5000_none_y_medium_hist_mean_0.9__20190128-233519_summary.csv')
# filenamez.append('Unitau_info_2_1a_sessao_sem_2_a_4_y_medium_hist_mean_1.0/log/Unitau_info_2_1a_sessao_sem_2_a_4_224_1.0_5000_none_y_medium_hist_mean_1.0__20190129-001221_summary.csv')

# base = 'y_medium_hist_std'
# filenamez.append('Unitau_info_2_1a_sessao_sem_2_a_4_y_medium_hist_std_0.1/log/Unitau_info_2_1a_sessao_sem_2_a_4_224_1.0_5000_none_y_medium_hist_std_0.1__20190128-180434_summary.csv')
# filenamez.append('Unitau_info_2_1a_sessao_sem_2_a_4_y_medium_hist_std_0.2/log/Unitau_info_2_1a_sessao_sem_2_a_4_224_1.0_5000_none_y_medium_hist_std_0.2__20190128-182650_summary.csv')
# filenamez.append('Unitau_info_2_1a_sessao_sem_2_a_4_y_medium_hist_std_0.3/log/Unitau_info_2_1a_sessao_sem_2_a_4_224_1.0_5000_none_y_medium_hist_std_0.3__20190129-083944_summary.csv')
# filenamez.append('Unitau_info_2_1a_sessao_sem_2_a_4_y_medium_hist_std_0.4/log/Unitau_info_2_1a_sessao_sem_2_a_4_224_1.0_5000_none_y_medium_hist_std_0.4__20190129-090712_summary.csv')
# filenamez.append('Unitau_info_2_1a_sessao_sem_2_a_4_y_medium_hist_std_0.5/log/Unitau_info_2_1a_sessao_sem_2_a_4_224_1.0_5000_none_y_medium_hist_std_0.5__20190129-094144_summary.csv')
# filenamez.append('Unitau_info_2_1a_sessao_sem_2_a_4_y_medium_hist_std_0.6/log/Unitau_info_2_1a_sessao_sem_2_a_4_224_1.0_5000_none_y_medium_hist_std_0.6__20190129-101933_summary.csv')
# filenamez.append('Unitau_info_2_1a_sessao_sem_2_a_4_y_medium_hist_std_0.7/log/Unitau_info_2_1a_sessao_sem_2_a_4_224_1.0_5000_none_y_medium_hist_std_0.7__20190129-105855_summary.csv')
# filenamez.append('Unitau_info_2_1a_sessao_sem_2_a_4_y_medium_hist_std_0.8/log/Unitau_info_2_1a_sessao_sem_2_a_4_224_1.0_5000_none_y_medium_hist_std_0.8__20190129-135742_summary.csv')
# filenamez.append('Unitau_info_2_1a_sessao_sem_2_a_4_y_medium_hist_std_0.9/log/Unitau_info_2_1a_sessao_sem_2_a_4_224_1.0_5000_none_y_medium_hist_std_0.9__20190129-154011_summary.csv')
# filenamez.append('Unitau_info_2_1a_sessao_sem_2_a_4_y_medium_hist_std_1.0/log/Unitau_info_2_1a_sessao_sem_2_a_4_224_1.0_5000_none_y_medium_hist_std_1.0__20190129-162101_summary.csv')

# base = 'y_medium_hist_var'
# filenamez.append('Unitau_info_2_1a_sessao_sem_2_a_4_y_medium_hist_var_0.1/log/Unitau_info_2_1a_sessao_sem_2_a_4_224_1.0_5000_none_y_medium_hist_var_0.1__20190129-105629_summary.csv')
# filenamez.append('Unitau_info_2_1a_sessao_sem_2_a_4_y_medium_hist_var_0.2/log/Unitau_info_2_1a_sessao_sem_2_a_4_224_1.0_5000_none_y_medium_hist_var_0.2__20190129-111838_summary.csv')
# filenamez.append('Unitau_info_2_1a_sessao_sem_2_a_4_y_medium_hist_var_0.3/log/Unitau_info_2_1a_sessao_sem_2_a_4_224_1.0_5000_none_y_medium_hist_var_0.3__20190129-115920_summary.csv')
# filenamez.append('Unitau_info_2_1a_sessao_sem_2_a_4_y_medium_hist_var_0.4/log/Unitau_info_2_1a_sessao_sem_2_a_4_224_1.0_5000_none_y_medium_hist_var_0.4__20190129-123730_summary.csv')
# filenamez.append('Unitau_info_2_1a_sessao_sem_2_a_4_y_medium_hist_var_0.5/log/Unitau_info_2_1a_sessao_sem_2_a_4_224_1.0_5000_none_y_medium_hist_var_0.5__20190129-132005_summary.csv')
# filenamez.append('Unitau_info_2_1a_sessao_sem_2_a_4_y_medium_hist_var_0.6/log/Unitau_info_2_1a_sessao_sem_2_a_4_224_1.0_5000_none_y_medium_hist_var_0.6__20190129-140901_summary.csv')
# filenamez.append('Unitau_info_2_1a_sessao_sem_2_a_4_y_medium_hist_var_0.6/log/Unitau_info_2_1a_sessao_sem_2_a_4_224_1.0_5000_none_y_medium_hist_var_0.6__20190129-142613_summary.csv')
# filenamez.append('Unitau_info_2_1a_sessao_sem_2_a_4_y_medium_hist_var_0.7/log/Unitau_info_2_1a_sessao_sem_2_a_4_224_1.0_5000_none_y_medium_hist_var_0.7__20190129-151425_summary.csv')
# filenamez.append('Unitau_info_2_1a_sessao_sem_2_a_4_y_medium_hist_var_0.8/log/Unitau_info_2_1a_sessao_sem_2_a_4_224_1.0_5000_none_y_medium_hist_var_0.8__20190129-155651_summary.csv')
# filenamez.append('Unitau_info_2_1a_sessao_sem_2_a_4_y_medium_hist_var_0.9/log/Unitau_info_2_1a_sessao_sem_2_a_4_224_1.0_5000_none_y_medium_hist_var_0.9__20190129-163714_summary.csv')


# base = 'y_medium_hist_median'
# filenamez.append('Unitau_info_2_1a_sessao_sem_2_a_4_y_medium_hist_median_0.1/log/Unitau_info_2_1a_sessao_sem_2_a_4_224_1.0_5000_none_y_medium_hist_median_0.1__20190129-105839_summary.csv')
# filenamez.append('Unitau_info_2_1a_sessao_sem_2_a_4_y_medium_hist_median_0.2/log/Unitau_info_2_1a_sessao_sem_2_a_4_224_1.0_5000_none_y_medium_hist_median_0.2__20190129-113155_summary.csv')
# filenamez.append('Unitau_info_2_1a_sessao_sem_2_a_4_y_medium_hist_median_0.3/log/Unitau_info_2_1a_sessao_sem_2_a_4_224_1.0_5000_none_y_medium_hist_median_0.3__20190129-121647_summary.csv')
# filenamez.append('Unitau_info_2_1a_sessao_sem_2_a_4_y_medium_hist_median_0.4/log/Unitau_info_2_1a_sessao_sem_2_a_4_224_1.0_5000_none_y_medium_hist_median_0.4__20190129-125847_summary.csv')
# filenamez.append('Unitau_info_2_1a_sessao_sem_2_a_4_y_medium_hist_median_0.5/log/Unitau_info_2_1a_sessao_sem_2_a_4_224_1.0_5000_none_y_medium_hist_median_0.5__20190129-134200_summary.csv')
# filenamez.append('Unitau_info_2_1a_sessao_sem_2_a_4_y_medium_hist_median_0.6/log/Unitau_info_2_1a_sessao_sem_2_a_4_224_1.0_5000_none_y_medium_hist_median_0.6__20190129-143548_summary.csv')
# filenamez.append('Unitau_info_2_1a_sessao_sem_2_a_4_y_medium_hist_median_0.6/log/Unitau_info_2_1a_sessao_sem_2_a_4_224_1.0_5000_none_y_medium_hist_median_0.6__20190129-162341_summary.csv')
# filenamez.append('Unitau_info_2_1a_sessao_sem_2_a_4_y_medium_hist_median_0.7/log/Unitau_info_2_1a_sessao_sem_2_a_4_224_1.0_5000_none_y_medium_hist_median_0.7__20190129-182357_summary.csv')
# filenamez.append('')
# filenamez.append('')



file_saida_temp = '{}{}'.format(dir_saidas, '{}_temp.csv'.format(base))
file_saida = '{}{}'.format(dir_saidas, '{}.csv'.format(base))
with open(file_saida_temp, 'w', newline='') as csvfile:
    spamwriter = csv.writer(csvfile, delimiter=';',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
    for f in filenamez:
        ok = []
        fail = []
        filename = '{}{}'.format(dir_exp, f)
        with open(filename, 'r') as csvfile:
            spamreader = csv.reader(csvfile, delimiter=';', quotechar='|')
            for row in spamreader:
                if row[2] == 'count_ok':
                    continue
                if int(row[2]) > 0:
                    ok.append(row)
                if int(row[5]) > 0:
                    fail.append(row)

        # nick;mean;count_ok;accu_mean_ok;thres_mean_ok;count_fail;accu_mean_fail;thres_mean_fail
        out = [None] * 8
        out[0] = ''
        out[1] = calc_mean(ok, 1)
        out[2] = calc_sum(ok, 2)
        out[3] = calc_mean(ok, 3)
        out[4] = calc_mean(ok, 4)
        out[5] = calc_sum(fail, 5)
        out[6] = calc_mean(fail, 6)
        out[7] = calc_mean(fail, 7)

        spamwriter.writerow(out)

with open(file_saida_temp, 'r') as temp:
    with open(file_saida, 'w') as saida:
        for line in temp.readlines():
            saida.writelines(line.replace('.', ','))

print('File generated: {}'.format(file_saida))
os.remove(file_saida_temp)