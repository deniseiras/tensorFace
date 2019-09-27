import cv2
import numpy as np
from matplotlib import pyplot
import os


def calculate_relative_iluminance(img):
    blue = img[:, :, 0]
    green = img[:, :, 1]
    red = img[:, :, 2]
    y = 0.2126 * red + 0.7152 * green + 0.0722 * blue
    return y.astype(int)

def calculate_relative_ilumminance_mean(img):
    y = calculate_relative_iluminance(img)
    return y.mean()


def calculate_relative_ilumminance_median(img):
    y = calculate_relative_iluminance(img)
    return np.median(y)


def calculate_relative_ilumminance_std(img):
    y = calculate_relative_iluminance(img)
    return y.std()


def calculate_relative_ilumminance_variance(img):
    y = calculate_relative_iluminance(img)
    return y.var()


def calculate_histogram(img):
    y = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    hist = cv2.calcHist([y], [0], None, [256], [0, 255])
    cv2.normalize(hist, hist, 0, 255, cv2.NORM_MINMAX)
    hist = hist.astype(int)
    return hist


def calculate_highkey_sum(h, highkey_min):
    highkey = h[highkey_min:255]
    highkey_f = highkey.sum()
    return highkey_f


def calculate_lowkey_sum(h, lowkey_max):
    lowkey = h[0:lowkey_max]
    lowkey_f = lowkey.sum()
    return lowkey_f


def calculate_medium_sum(h, lowkey_max, highkey_min):
    medim_key = h[lowkey_max + 1: highkey_min - 1]
    mediumkey_f = medim_key.sum()
    mediumkey_f = 1 if mediumkey_f == 0 else mediumkey_f
    return mediumkey_f


def calculate_shadow_factor(h, lowkey_max, highkey_min):
    lk = calculate_lowkey_sum(h, lowkey_max)
    mk = calculate_medium_sum(h, lowkey_max, highkey_min)
    factor = mk / lk if lk > 0 else mk
    return factor


def calculate_highlight_factor(h, lowkey_max, highkey_min):
    hk = calculate_highkey_sum(h, highkey_min)
    mk = calculate_medium_sum(h, lowkey_max, highkey_min)
    factor = mk / hk if hk > 0 else mk
    return factor


def calculate_medium_std(h, lowkey_max, highkey_min):
    medim_key = h[lowkey_max + 1: highkey_min - 1]
    return medim_key.std()



# img = cv2.imread('/media/denis/dados/dev/face_bds_changed/Unitau_info_2_1a_sessao_sem_2_a_4_y_highlight_factor_1.0_thres_ok/heltonsilva/IMG_2007.JPG')
img = cv2.imread('/media/denis/dados/dev/face_bds_changed/Unitau_info_2_1a_sessao_sem_2_a_4_y_mean_0.1_thres_fail/allexsousa/2.jpg')

import time
a = time.time()
lowkey_max = 85
highkey_min = 170
h = calculate_histogram(img)
print(calculate_shadow_factor(h, lowkey_max, highkey_min))
# print(calculate_relative_ilumminance_median(img))
print(time.time() - a)



# low_max = 85
# high_min = 170
# import csv
# file_tmp = '/media/denis/dados/dev/hilowkeys_y_TEMP.csv'
# file_saida = '/media/denis/dados/dev/hilowkeys_y.csv'
# with open(file_tmp, 'w', newline='') as csvfile:
#     spamwriter = csv.writer(csvfile, delimiter=';',
#                             quotechar='|', quoting=csv.QUOTE_MINIMAL)
#
#     # test_dir = '/media/denis/dados/dev/face_bds_changed/Unitau_info_2_1a_sessao_sem_2_a_4_y_median_0.3_thres_ok'
#     test_dir = '/media/denis/dados/face_bds/Unitau_info_2'
#     # person_dir = '/media/denis/dados/dev/face_bds_changed/Unitau_info_2_1a_sessao_sem_2_a_4_y_median_0.3_thres_ok'
#
#     spamwriter.writerow(['file', 'shape' ,'min', 'max' ,'mean', 'var', 'std', 'median', 'zeros', 'v255', 'shadow', 'highlight', 'medium_std'])
#     for person_name in os.listdir(test_dir):
#         person_path_new = os.path.join(test_dir, person_name)
#     # person_path_new = person_dir
#         for face_file_name in [f for f in os.listdir(person_path_new) if
#                                os.path.isfile(os.path.join(person_path_new, f))]:
#             face_file_w_path = os.path.join(person_path_new, face_file_name)
#             img = cv2.imread(face_file_w_path)
#             y = calculate_relative_iluminance(img)
#             h = calculate_histogram(img)
#             # unique, counts = np.unique(y, return_counts=True)
#             unique, counts = np.unique(h, return_counts=True)
#             dic = dict(zip(unique, counts))
#             zeros = dic[0] if 0 in dic.keys() else 0
#             v255 = dic[255] if 255 in dic.keys() else 0
#             shadow = calculate_shadow_factor(h, low_max, high_min)
#             highlight = calculate_highlight_factor(h, low_max, high_min)
#             medium_std = calculate_medium_std(h, low_max, high_min)
#             # zeros = dic[0] if 0 in dic.keys() else 0
#             # v255 = dic[255] if 255 in dic.keys() else 0
#             out = [None] * 13
#             out[0] = face_file_w_path
#             out[1] = y.shape
#             out[2] = y.min()
#             out[3] = y.max()
#             out[4] = y.mean()
#             out[5] = y.var()
#             out[6] = y.std()
#             out[7] = np.median(y)
#             out[8] = zeros
#             out[9] = v255
#             out[10] = shadow
#             out[11] = highlight
#             out[12] = medium_std
#             spamwriter.writerow(out)
#
# with open(file_tmp, 'r') as temp:
#     with open(file_saida, 'w') as saida:
#         for line in temp.readlines():
#             saida.writelines(line.replace('.', ','))
#
# os.remove(file_tmp)

# pyplot.hist(y)
# pyplot.show()


# img_yuv = cv2.cvtColor(img, cv2.COLOR_BGR2YUV)
    # y = img_yuv[:,:,0]

    # print('img mean = ', np.median(y))
    # print('img rmse = ', np.sqrt(np.mean((10-y)**2)) )
    #
    # print('img mean = ', np.mean(y))
    # print('img var = ', np.var(y))
    # print('img std = ', np.std(y))
    # hist = cv2.calcHist([img], [0], None, [256], [0,256])
    # print(hist)

    # print('hist mean = ', np.mean(hist))
    # print('hist var = ', np.var(hist))
    # print('hist std = ', np.std(hist))
    # print('Hist Ilumnin ...')
    # cv2.imshow('Original Image', img)
    # cv2.waitKey(1000)
    # pyplot.hist(y)
    # pyplot.show()
    #
    # # equalize the histogram of the Y channel
    # img_yuv[:, :, 0] = cv2.equalizeHist(y)
    # # convert the YUV image back to RGB format
    # img_output = cv2.cvtColor(img_yuv, cv2.COLOR_YUV2BGR)
    # print('out mean = ', np.mean(img_output))
    # print('out var = ', np.var(img_output))
    # print('out std = ', np.std(img_output))
    # cv2.destroyAllWindows()
    # print('Hist Ilumnin equalized ...')
    # pyplot.hist(y)
    # pyplot.show()


# face_file_w_path = '/media/denis/dados/dev/face_bds_changed/Unitau_info_2_1a_sessao_sem_2_a_4_y_std_0.1_thres_ok/eitorgiacomozzi/suspect_20181122-193758_36.jpg'
# face_file_w_path = '/media/denis/dados/dev/face_bds_changed/Unitau_info_2_1a_sessao_sem_2_a_4_y_std_0.1_thres_ok/eitorgiacomozzi/suspect_20181122-193758_59.jpg'
# face_file_w_path = '/media/denis/dados/dev/face_bds_changed/Unitau_info_2_1a_sessao_sem_2_a_4_y_std_0.1_thres_ok/eitorgiacomozzi/suspect_20181122-193831_31.jpg'
# face_file_w_path = '/media/denis/dados/dev/face_bds_changed/Unitau_info_2_1a_sessao_sem_2_a_4_y_std_0.1_thres_fail/eitorgiacomozzi/suspect_20181122-193758_27.jpg'
# face_file_w_path = '/media/denis/dados/dev/face_bds_changed/Unitau_info_2_1a_sessao_sem_2_a_4_y_std_0.1_thres_fail/eitorgiacomozzi/suspect_20181122-193831_13.jpg'
