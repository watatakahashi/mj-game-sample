from modules.convert_private_tehai import convert,\
    convert_to_pai_type_dimension, convert_discard, convert_safety
import numpy as np
import sys
sys.path.append('/content/drive/My Drive/麻雀/麻雀AI')


# 手牌のエンコード

def encode_tehai(tehai):
    converted = np.array(convert(tehai))
    converted = converted.transpose()
    return converted

# 捨て牌と副露のエンコード


def encode_discard(
        myPlayerDiscard,
        lowerPlayerDiscard,
        oppositePlayerDiscard,
        upperPlayerDiscard):
    my = np.array(convert_discard(myPlayerDiscard))
    my = my.transpose()

    lower = np.array(convert_discard(lowerPlayerDiscard))
    lower = lower.transpose()

    opposite = np.array(convert_discard(oppositePlayerDiscard))
    opposite = opposite.transpose()

    upper = np.array(convert_discard(upperPlayerDiscard))
    upper = upper.transpose()
    return np.vstack([my, lower, opposite, upper])

# ドラ表示牌のエンコード


def encode_dora(dora):
    dora_pai_type = convert_to_pai_type_dimension(dora)
    dora_feature = np.array([dora_pai_type])
    return dora_feature

# 対象プレイヤーのエンコード(0=東家, 1=南家,...)


def encode_player(category_num):
    return np.array([np.ones(37) if i == category_num else np.zeros(37)
                    for i in range(4)])

# リーチのエンコード


def encode_reach(category_list):
    return np.array([np.ones(37) if i == 1 else np.zeros(37)
                    for i in category_list])

# 場風のエンコード


def encode_bakaze(category_num):
    return np.array([np.ones(37) if i == category_num else np.zeros(37)
                    for i in range(3)])

# 局数のエンコード


def encode_kyoku(category_num):
    return np.array([np.ones(37) if i == category_num else np.zeros(37)
                    for i in range(4)])

# 持ち点のエンコード


def encode_point(my_point, target_point):
    diff = my_point - target_point
    bins = [-12000, -10000, -8000, -4000, -
            1000, 0, 1000, 4000, 8000, 10000, 12000]
    which_bin = np.digitize(diff, bins=bins)
    point_array = [np.ones(37) if i == which_bin else np.zeros(37)
                   for i in range(len(bins) + 1)]
    return np.array(point_array)

# 安全牌のエンコード


def encode_safety(safety_str_list):
    return np.array([convert_safety(i) for i in safety_str_list])
