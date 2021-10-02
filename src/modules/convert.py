import numpy as np
import tensorflow as tf
from tensorflow.keras.utils import to_categorical

# 数字が先の牌文字用
# pai_list = ['0m','1m','2m','3m','4m','5m','6m','7m','8m','9m',
#     '0p','1p','2p','3p','4p','5p','6p','7p','8p','9p',
#     '0s','1s','2s','3s','4s','5s','6s','7s','8s','9s',
#     '1z','2z','3z','4z','5z','6z','7z']

pai_list = ['m0','m1','m2','m3','m4','m5','m6','m7','m8','m9',
    'p0','p1','p2','p3','p4','p5','p6','p7','p8','p9',
    's0','s1','s2','s3','s4','s5','s6','s7','s8','s9',
    'z1','z2','z3','z4','z5','z6','z7', '']

def convert_pai(pai_str):
    return pai_list.index(pai_str)

def reverse_convert_pai(pai_num):
    return pai_list[pai_num]

def split_pai(tehai, n):
    r = [tehai[i: i+n] for i in range(0, len(tehai), n)]
    return r

def convert_tehai(tehai):
    splited = split_pai(tehai, 2)
    converted_list = list(map(convert_pai, splited))
    if len(converted_list) < 14:
        converted_list.extend([37] * (14 - len(converted_list)))
    return converted_list

def convert_tehai_dummies(tehai):
    converted = convert_tehai(tehai)
    categoricaled = np.array(to_categorical(converted, 38, dtype='int'))
    categoricaled_list = categoricaled.flatten()
    return categoricaled_list