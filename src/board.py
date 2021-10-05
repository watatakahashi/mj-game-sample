from dataclasses import dataclass, field
import random
import pandas as pd
from modules.agari_check import agari_check, can_reach


@dataclass
class Board:

    # 学習者
    learner: int

    # ゲーム終了フラグ
    is_end_of_game: bool = False

    # ツモ者
    tsumo_player: int = 0

    # 最終ツモ
    latest_tsumo: str = None

    # 最終打牌
    latest_dahai: str = None

    # 手牌
    private_tiles: list = field(default_factory=list)

    # 山
    wall_tiles: list = field(default_factory=list)

    # 捨て牌
    discards: list = field(default_factory=list)

    # リーチ可否
    reaches: list = field(default_factory=list)

    # ドラ表示牌
    dora_open: str = None

    def start_kyoku(self):
        """
        局を開始する
        """
        self.__init_wall_tiles()

        INIT_TEHAI_NUM = 13
        self.private_tiles = [[], [], [], []]
        self.private_tiles[0] = self.wall_tiles[0:INIT_TEHAI_NUM]
        self.private_tiles[1] = self.wall_tiles[INIT_TEHAI_NUM:INIT_TEHAI_NUM * 2]
        self.private_tiles[2] = self.wall_tiles[INIT_TEHAI_NUM *
                                                2:INIT_TEHAI_NUM * 3]
        self.private_tiles[3] = self.wall_tiles[INIT_TEHAI_NUM *
                                                3:INIT_TEHAI_NUM * 4]

        self.wall_tiles = self.wall_tiles[INIT_TEHAI_NUM * 4:]

        self.discards = [[], [], [], []]

        self.reaches = [False, False, False, False]

        self.dora_open = self.wall_tiles.pop(0)

        # 第一ツモ
        self.tsumo()

    def next_player(self):
        # 次のプレイヤーの手番に移動する
        self.tsumo_player = (self.tsumo_player + 1 + 4) % 4

    def is_tsumo_player_reach(self):
        """
        ツモ者がリーチしているかどうかを確認する
        """
        return self.reaches[self.tsumo_player]

    def tsumo(self):
        """
        ツモ、ツモアガリ判定を行い、手牌にツモ牌を加える
        """
        self.latest_tsumo = self.wall_tiles.pop(0)

        # 上がり判定を行う
        result = agari_check(self.private_tiles[self.tsumo_player],
                             self.latest_tsumo,
                             is_tsumo=True,
                             is_riichi=self.reaches[self.tsumo_player])
        if result.yaku is not None:
            print('ツモ和了', result, result.yaku)
            # TODO: 上がった瞬間一旦ゲームを終了する
            self.is_end_of_game = True

        self.private_tiles[self.tsumo_player] += [self.latest_tsumo]

    def dahai(self, hai):
        """
        手牌から打牌を取り除く、ロン和了の判定を行う、リーチ判定をする、河に打牌を追加する
        リーチ時はツモ切り
        """
        if self.reaches[self.tsumo_player]:
            self.private_tiles[self.tsumo_player].remove(self.latest_tsumo)
        else:
            self.private_tiles[self.tsumo_player].remove(hai)

        self.latest_dahai = hai
        self.__check_ron_agari()

        # TODO: 一旦リーチできるならリーチする
        # シャンテン数
        is_reach = not self.reaches[self.tsumo_player] and can_reach(
            self.private_tiles[self.tsumo_player])
        if is_reach:
            print('リーチする', self.tsumo_player, is_reach)
            self.reaches[self.tsumo_player] = True

        # 河に追加
        self.discards[self.tsumo_player] += [hai]

    def __check_ron_agari(self):
        """
        打牌者以外の3人がロン和了可能かどうかをチェックする
        """
        for i in range(3):
            player = (self.tsumo_player + (i + 1) + 4) % 4
            result = agari_check(
                tehai=self.private_tiles[player],
                tsumo=self.latest_dahai,
                is_tsumo=False,
                is_riichi=self.reaches[player])

            # TODO: 現在一人ずつロンチェックしているので、ダブロンに対応する
            if result.yaku is not None:
                print('ロン和了', result, result.yaku)
                self.is_end_of_game = True

    def __init_wall_tiles(self):
        """
        山を初期化する
        """
        pass
        self.wall_tiles = HAI_LIST * 4
        random.shuffle(self.wall_tiles)

    def generate_state_record(self):
        df = pd.DataFrame([[
            self.tsumo_player,  # TODO: 親番を0とするので調整する
            ''.join(self.private_tiles[self.tsumo_player]),  # ツモ番のプレイヤー
            ''.join(self.discards[(self.tsumo_player + 4) % 4]),
            ''.join(self.discards[(self.tsumo_player + 4 + 1) % 4]),
            ''.join(self.discards[(self.tsumo_player + 4 + 2) % 4]),
            ''.join(self.discards[(self.tsumo_player + 4 + 3) % 4]),
            0,
            0,
            self.dora_open,
            0,
            self.discards[(self.tsumo_player + 4 + 1) % 4],
            self.discards[(self.tsumo_player + 4 + 2) % 4],
            self.discards[(self.tsumo_player + 4 + 3) % 4],
            '',
            '',
            '',
            '',
            25000,
            25000,
            25000,
            25000,
            '',
            '',
            '',
            '',
            '1z',
        ]], columns=COLMUN)
        return df


HAI_LIST = ['1m', '2m', '3m', '4m', '5m', '6m', '7m', '8m', '9m',
            '1p', '2p', '3p', '4p', '5p', '6p', '7p', '8p', '9p',
            '1s', '2s', '3s', '4s', '5s', '6s', '7s', '8s', '9s',
            '1z', '2z', '3z', '4z', '5z', '6z', '7z']

COLMUN = [
    'player',
    'privateTehaiString',
    'myPlayerDiscard',
    'lowerPlayerDiscard',
    'oppositePlayerDiscard',
    'upperPlayerDiscard',
    'bakaze',
    'kyokuNum',
    'doraOpen',
    'isMyPlayerReach',
    'isLowerPlayerReach',
    'isOppositePlayerReach',
    'isUpperPlayerReach',
    'myPlayerMeld',
    'lowerPlayerMeld',
    'oppositePlayerMeld',
    'upperPlayerMeld',
    'myPlayerPoints',
    'lowerPlayerPoints',
    'oppositePlayerPoints',
    'upperPlayerPoints',
    'myPlayerSafetyTile',
    'lowerPlayerSafetyTile',
    'oppositePlayerSafetyTile',
    'upperPlayerSafetyTile',
    'selectedPai',
]
