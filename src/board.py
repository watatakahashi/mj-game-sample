from dataclasses import dataclass, field
import random
from typing import List
import pandas as pd
from modules.agari_check import agari_check, can_reach
from modules.utils import sort_tehai

# 本来は14枚だがドラ表示牌を物理的に取り除くため一旦1枚減らしている
# 厳密には変数になる
MIN_LEAVE_WALL_COUNT = 13


@dataclass
class Board:
    """
    盤面クラス
    外側から操作できる処理
    - ツモ
    - 打牌
    """

    # 学習者
    learner: int

    # 0:打牌, 1:リーチ, 2:アクション
    use_model: int = 0

    # 学習データ
    training_data = pd.DataFrame()

    # ゲーム終了フラグ
    is_end_of_game: bool = False

    # 局終了フラグ
    is_end_of_kyoku: bool = False

    # 場風(0~2)
    bakaze: int = 0

    # 局数(0~3) = 現在親番のプレイヤー
    kyoku_num: int = 0

    # ツモ者
    tsumo_player: int = 0

    # 最終ツモ
    latest_tsumo: str = None

    # 最終打牌
    latest_dahai: str = '1z'  # TODO: 開局第一ツモに対応

    # 手牌
    private_tiles: List[str] = field(default_factory=list)

    # 山
    wall_tiles: list = field(default_factory=list)

    # 捨て牌
    discards: list = field(default_factory=list)

    # リーチ可否
    reaches: list = field(default_factory=list)

    # 得点、東1局親番をindex=0とする
    points: list = field(default_factory=list)

    # ドラ表示牌
    dora_open: str = None

    def __post_init__(self):
        self.start_kyoku()

    def start_kyoku(self):
        """
        局を開始する
        """
        print(f'{self.bakaze}-{self.kyoku_num}を開始')
        if self.bakaze == 0 and self.kyoku_num == 0:
            self.__start_game()

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

        # 局数が最初にツモる親番プレイヤーとなるため
        self.tsumo_player = self.kyoku_num

        # 第一ツモ
        self.tsumo()

    def __start_game(self):
        """
        ゲーム開始処理
        """
        self.points = [25000, 25000, 25000, 25000]

    def __next_player(self):
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
            self.is_end_of_kyoku = True

        self.private_tiles[self.tsumo_player] += [self.latest_tsumo]

        if len(self.private_tiles[self.tsumo_player]) not in [
                5, 8, 11, 14]:
            raise ValueError(
                f'手牌の長さが不正 hai={self.private_tiles[self.tsumo_player]}')

        if self.is_end_of_kyoku:
            self.__end_of_kyoku()

        self.use_model = 0

    def dahai(self, hai):
        """
        手牌から打牌を取り除く、ロン和了の判定を行う、リーチ判定をする、河に打牌を追加する
        リーチ時はツモ切り
        最後に局終了処理、または次のプレイヤーのツモを行う
        """

        if len(hai) != 2:
            raise ValueError(f'打牌の長さが不正 hai={hai}')
        if len(self.private_tiles[self.tsumo_player]) not in [5, 8, 11, 14]:
            raise ValueError(
                f'手牌の長さが不正 hai={self.private_tiles[self.tsumo_player]}',
                self)

        # 学習者かつリーチでない場合はデータの保存
        if self.tsumo_player == self.learner and not self.is_tsumo_player_reach():
            self.__save_data(hai)

        if self.is_tsumo_player_reach():
            self.latest_dahai = self.latest_tsumo
        else:
            self.latest_dahai = hai

        try:
            self.private_tiles[self.tsumo_player].remove(self.latest_dahai)
        except BaseException:
            raise ValueError(
                '手牌にない牌を選択 ',
                'プレイヤー', self.tsumo_player,
                '手牌=', self.private_tiles[self.tsumo_player],
                'ツモ=', self.latest_dahai)

        self.__check_ron_agari()

        if self.is_end_of_kyoku:
            self.__end_of_kyoku()
            return

        # リーチできるかどうかの確認、できる場合は一旦終了
        is_reach = not self.reaches[self.tsumo_player] and can_reach(
            self.private_tiles[self.tsumo_player])
        if is_reach:
            self.use_model = 1
            return

        self.after_dahai()

    def after_dahai(self, is_reach=False):
        """
        河に追加からの処理
        """
        if is_reach:
            self.reaches[self.tsumo_player] = True

        # 河に追加
        self.discards[self.tsumo_player] += [self.latest_dahai]

        # ツモ番がない場合は流局
        if len(self.wall_tiles) <= MIN_LEAVE_WALL_COUNT:
            print('流局')
            self.is_end_of_kyoku = True

        # TODO:アクションできるかどうかの確認、できる場合は一旦終了
        can_action = True
        if can_action:
            self.use_model = 2
            return

        self.after_action()

    def after_action(self, player=None, action=None):
        """
        アクションの処理から
        """

        if action is not None:
            # TODO: アクション実行
            # アクション者に手番を指定して打牌に移動
            self.tsumo_player = player
            self.use_model = 0
            return

        if self.is_end_of_kyoku:
            self.__end_of_kyoku()
        else:
            self.__next_player()
            self.tsumo()

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
                self.is_end_of_kyoku = True

    def __init_wall_tiles(self):
        """
        山を初期化する
        """
        pass
        self.wall_tiles = HAI_LIST * 4
        random.shuffle(self.wall_tiles)

    def __end_of_kyoku(self):
        """
        局終了時の処理
        """
        self.is_end_of_kyoku = False

        self.kyoku_num += 1
        if self.kyoku_num > 3:
            self.bakaze += 1
            self.kyoku_num = 0

        # 反時計回りに席移動
        self.learner = (self.learner - 1 + 8) % 4

        # ゲーム終了判定、一旦西入は考慮しない
        if self.bakaze == 2:
            self.is_end_of_game = True
        else:
            self.start_kyoku()

    def generate_state_record(self):
        """
        局面レコードを取得する
        """
        df = pd.DataFrame([[
            self.tsumo_player,  # TODO: 親番を0とするので調整する
            # ツモ番のプレイヤー
            ''.join(sort_tehai(self.private_tiles[self.tsumo_player])),
            ''.join(self.discards[(self.tsumo_player + 4 + 0) % 4]),
            ''.join(self.discards[(self.tsumo_player + 4 + 1) % 4]),
            ''.join(self.discards[(self.tsumo_player + 4 + 2) % 4]),
            ''.join(self.discards[(self.tsumo_player + 4 + 3) % 4]),
            self.bakaze,
            self.kyoku_num,
            self.dora_open,
            0,
            1 if self.reaches[(self.tsumo_player + 4 + 1) % 4] else 0,
            1 if self.reaches[(self.tsumo_player + 4 + 2) % 4] else 0,
            1 if self.reaches[(self.tsumo_player + 4 + 3) % 4] else 0,
            '',
            '',
            '',
            '',
            self.points[(self.tsumo_player + 4 + 0) % 4],
            self.points[(self.tsumo_player + 4 + 1) % 4],
            self.points[(self.tsumo_player + 4 + 2) % 4],
            self.points[(self.tsumo_player + 4 + 3) % 4],
            '',
            '',
            '',
            '',
            '1z',  # yなので不要
        ]], columns=COLMUN)

        return df

    def generate_reach_state_record(self):
        """
        リーチ用、局面レコードを取得する
        """
        df = self.generate_state_record()
        df['selectedPai'] = self.latest_dahai
        df['isReach'] = 0  # 　yなので不要

        # NOTE: 先に打牌をしているので一旦手動で追加
        if len(df.privateTehaiString.values[0]) != 13 * 2:
            raise ValueError(
                f'手牌の長さが不正 {df.privateTehaiString.values[0]}')

        df['privateTehaiString'] = df['privateTehaiString'] + self.latest_dahai

        return df

    def generate_action_state_record(self, player):
        """
        アクション用、局面レコードを取得する
        """
        df = self.generate_state_record()
        # TODO: playerに応じて視点の変更をする
        df['player'] = player
        df['selectedPai'] = self.latest_dahai
        df['dahaiPlayer'] = self.tsumo_player
        df['action'] = 0  # y

        return df

    def __save_data(self, hai):
        record = self.generate_state_record()
        record['selectedPai'] = hai
        self.training_data = self.training_data.append(record)


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
