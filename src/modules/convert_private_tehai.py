import numpy as np
import re

PAI_LIST = ['0m', '1m', '2m', '3m', '4m', '5m', '6m', '7m', '8m', '9m',
            '0p', '1p', '2p', '3p', '4p', '5p', '6p', '7p', '8p', '9p',
            '0s', '1s', '2s', '3s', '4s', '5s', '6s', '7s', '8s', '9s',
            '1z', '2z', '3z', '4z', '5z', '6z', '7z']


# 牌を4次元リストに変換する
# 例 1mが3枚ある→[1,1,1,0]
def convert_to_forth_dimension(pai_type, tehai):
    count = len(re.findall(pai_type, tehai))
    if count == 0:
        return[0, 0, 0, 0]
    elif count == 1:
        return[1, 0, 0, 0]
    elif count == 2:
        return[1, 1, 0, 0]
    elif count == 3:
        return[1, 1, 1, 0]
    elif count == 4:
        return[1, 1, 1, 1]
    else:
        raise ValueError(f'5枚以上の牌がある tehai={tehai} pai_type={pai_type}')

# 37種類の牌をOneHotEncodingして1行の配列を返す
# 例 1m→[0,1,0,0,....]


def convert_to_pai_type_dimension(pai_str):
    pai_num = convert_selected_pai_to_num(pai_str)
    pai_list = [0] * 37
    pai_list[pai_num] = 1
    return pai_list

# 文字列→数値の変換
# 例 1m1m1m2m2m4m→[[1,1,1,0],[1,1,0,0],[0,0,0,0],[1,0,0,0],...]


def convert(tehai):
    mapped = list(
        map(lambda pai_type: convert_to_forth_dimension(pai_type, tehai), PAI_LIST))
    return mapped

# 1牌を数値に変換
# 例 1m→1 3m→3 7z→36


def convert_selected_pai_to_num(pai_str):
    return PAI_LIST.index(pai_str)


# 数値→文字列の変換
# 例 1→1m 36→7z
def reverse_convert_pai(pai_num):
    return PAI_LIST[pai_num]

# 例 [[1,1,1,0],[1,1,0,0],[0,0,0,0],[1,0,0,0],...]→1m1m1m2m2m4m


def reverse_convert(tehai):
    reshaped = tehai.reshape(-1, 4)
    count_list = list(map(lambda x: np.count_nonzero(x == 1), reshaped))
    res_str = ''
    for i in range(len(PAI_LIST)):
        res_str = res_str + PAI_LIST[i] * count_list[i]
    return res_str

# 河情報を配列に変換する
# 例 1m2m2m4m1m1m(順不同)→[[1,1,1,0],[1,1,0,0],[0,0,0,0],[1,0,0,0],...]


def convert_discard(discard_str):
    return convert(discard_str)

# 例 1m2m4m(順不同)→[0,1,1,0,1,...]


def one_hot_func(pai_type, pai_str):
    return 1 if pai_type in pai_str else 0


def convert_safety(safety_str):
    # 01変換
    # 37種類を変換
    mapped = list(map(lambda pai_type: one_hot_func(
        pai_type, safety_str), PAI_LIST))

    return mapped
