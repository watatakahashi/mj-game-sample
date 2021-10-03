from dataclasses import dataclass, field
import random
import time
import numpy as np
import pandas as pd

@dataclass
class Board:
    learner: int
    tsumo_player: int = 0
    private_tiles: list = field(default_factory=list)
    wall_tiles: list = field(default_factory=list)
    
    def start_kyoku(self):
        """
        局を開始する
        """
        self.__init_wall_tiles()

        INIT_TEHAI_NUM = 13
        self.private_tiles = [[],[],[],[]]
        self.private_tiles[0] = self.wall_tiles[0:INIT_TEHAI_NUM]
        self.private_tiles[1] = self.wall_tiles[INIT_TEHAI_NUM:INIT_TEHAI_NUM * 2]
        self.private_tiles[2] = self.wall_tiles[INIT_TEHAI_NUM * 2:INIT_TEHAI_NUM * 3]
        self.private_tiles[3] = self.wall_tiles[INIT_TEHAI_NUM * 3:INIT_TEHAI_NUM * 4]
        self.wall_tiles = self.wall_tiles[INIT_TEHAI_NUM * 4:]

        # 第一ツモ
        self.tsumo()
    
    def next_player(self):
        self.tsumo_player = (self.tsumo_player + 1 + 4) % 4

    def tsumo(self):
        # 手牌にツモを加える
        tsumo_hai = self.wall_tiles.pop(0)
        self.private_tiles[self.tsumo_player] += [tsumo_hai]
    
    def dahai(self, hai):
        # 打牌を行い手牌から取り除く
        self.private_tiles[self.tsumo_player].remove(hai)

    def __init_wall_tiles(self):
        """
        山を初期化する
        """
        pass
        self.wall_tiles = HAI_LIST * 4
        random.shuffle(self.wall_tiles)
    
    def generate_state_record(self):
        df = pd.DataFrame([[
        0,
        ''.join(self.private_tiles[self.tsumo_player]), # ツモ番のプレイヤー
        '',
        '',
        '',
        '',
        0,
        0,
        '1z',
        0,
        0,
        0,
        0,
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

COLMUN=['player', 'privateTehaiString', 'myPlayerDiscard', 'lowerPlayerDiscard',
        'oppositePlayerDiscard', 'upperPlayerDiscard', 'bakaze',
        'kyokuNum', 'doraOpen', 'isMyPlayerReach',
        'isLowerPlayerReach', 'isOppositePlayerReach', 'isUpperPlayerReach',
        'myPlayerMeld', 'lowerPlayerMeld', 'oppositePlayerMeld',
        'upperPlayerMeld', 'myPlayerPoints', 'lowerPlayerPoints',
        'oppositePlayerPoints', 'upperPlayerPoints',
        'myPlayerSafetyTile', 'lowerPlayerSafetyTile', 'oppositePlayerSafetyTile', 'upperPlayerSafetyTile',
        'selectedPai',
        ]