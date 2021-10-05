# 麻雀ライブラリ
from mahjong.hand_calculating.hand import HandCalculator
# from mahjong.meld import Meld
from mahjong.hand_calculating.hand_config import HandConfig, OptionalRules
from mahjong.shanten import Shanten
from mahjong.tile import TilesConverter


def agari_check(tehai, tsumo, is_tsumo, is_riichi=False):
    if len(tehai) not in [4, 7, 10, 13]:
        raise ValueError('手牌の長さが不正です tehai=', tehai)
    # NOTE: 和了判定はツモを手牌に加える必要があるので、一度加える
    tehai_and_tsumo = tehai + [tsumo]

    tehai_manpinsou_dict = get_manpinsou_dict(tehai_and_tsumo)

    tiles = TilesConverter.string_to_136_array(
        man=tehai_manpinsou_dict['m'],
        pin=tehai_manpinsou_dict['p'],
        sou=tehai_manpinsou_dict['s'],
        honors=tehai_manpinsou_dict['h'],
        has_aka_dora=True)

    tsumo_manpinsou_dict = get_manpinsou_dict([tsumo])

    win_tile = TilesConverter.string_to_136_array(
        man=tsumo_manpinsou_dict['m'],
        pin=tsumo_manpinsou_dict['p'],
        sou=tsumo_manpinsou_dict['s'],
        honors=tsumo_manpinsou_dict['h'],
        has_aka_dora=True)[0]

    calculator = HandCalculator()

    # print('手牌: ', tehai_manpinsou_dict, 'ツモor他家打牌: ', tsumo_manpinsou_dict)

    result = calculator.estimate_hand_value(
        tiles, win_tile, config=HandConfig(
            is_tsumo=is_tsumo, is_riichi=is_riichi, options=OptionalRules(
                has_open_tanyao=True, has_aka_dora=True)))

    # if result.yaku is not None:

    return result


def can_reach(tehai):
    shanten = Shanten()

    tehai_manpinsou_dict = get_manpinsou_dict(tehai)

    tiles = TilesConverter.string_to_34_array(
        man=tehai_manpinsou_dict['m'].replace('0', '5'),
        pin=tehai_manpinsou_dict['p'].replace('0', '5'),
        sou=tehai_manpinsou_dict['s'].replace('0', '5'),
        honors=tehai_manpinsou_dict['h']
    )
    shanten = shanten.calculate_shanten(tiles)
    # print('手牌: ', tehai_manpinsou_dict, 'シャンテン数: ',shanten)
    return shanten == 0


def get_manpinsou_dict(tehai):
    manpinsou_dict = {'m': '', 'p': '', 's': '', 'h': ''}
    # 手牌を変換
    # 例えばtehai=[1m, 2m]と持っている場合、manpinsou_dict={m:12}となる
    for hai in tehai:
        for hai_type in ['m', 'p', 's']:
            if hai_type in hai:
                manpinsou_dict[hai_type] += hai[0]
        if 'z' in hai:
            manpinsou_dict['h'] += hai[0]
    return manpinsou_dict
