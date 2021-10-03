from dataclasses import dataclass, field
# from board import Board
import random
import time
from predict import Predictor
import numpy as np
import pandas as pd

@dataclass
class Worker:
    # board: list = field(default_factory=list)

    def run_games(self, learner, opponent, num_games=1):
        # states = [Game(Board()) for _ in range(num_games)]
        # idxs_to_unfinished_states = [{'state': states[i], 'learner': (i + 4) % 4} for i in range(num_games)]
        idxs_to_unfinished_states = [Board(learner=(i + 4) % 4) for i in range(num_games)]

        # 東1局を開始する
        [state.start_kyoku() for state in idxs_to_unfinished_states]

        # while len(idxs_to_unfinished_states) > 0:
        for i in range(70):
            # print('順目', i)

            # 自分のツモ番
            # learner_states = list(filter(lambda state: state['state'].tsumo_player() == state['learner'], idxs_to_unfinished_states))
            learner_states = list(filter(lambda state: state.tsumo_player == state.learner, idxs_to_unfinished_states))
            dahais = learner.get_dahai(learner_states)

            # 状態の更新
            for state, dahai in zip(learner_states, dahais):
                state.dahai(dahai)
                pass
                # TODO: 打牌に対するアクション
            
            # 自分以外のツモ番
            not_learner_state = list(filter(lambda state: state.tsumo_player != state.learner, idxs_to_unfinished_states))
            dahais = opponent.get_dahai(not_learner_state)
            
            # 状態の更新
            for state, dahai in zip(not_learner_state, dahais):
                state.dahai(dahai)
                pass
                # TODO: 打牌に対するアクション

            # 手番の更新とツモまで行う
            for state in idxs_to_unfinished_states:
                state.next_player()
                state.tsumo()
        # print(idxs_to_unfinished_states)


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
        ''.join(self.private_tiles[self.tsumo_player]),
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

HAI_LIST_RED = HAI_LIST + ['0m', '0p', '0s']

@dataclass
class Game:
    # 学習者
    learner: int
    board: Board
    points: list = field(default_factory=list)

    def __post_init__(self):
        self.points = [25000, 25000, 25000, 25000]

    def next_player(self):
        self.board.next_player()
        
    def tsumo_player(self):
        return self.board.tsumo_player

    def tsumo(self):
        self.board.tsumo()

@dataclass
class Player:
    clf = Predictor()

    def get_dahai(self, states):
        # 打牌を決定する、手牌からは取り除かない
        records = pd.DataFrame()
        for state in states:
            records = records.append(state.generate_state_record())
        print('records.shape', records.shape)
        
        start = time.time()
        max_indexes = self.clf.multi_predict(records)
        elapsed_time = time.time() - start
        print ("予測実行時間:{0}".format(elapsed_time) + "[sec]")

        dahais = [random.choice(s.private_tiles[s.tsumo_player]) for s in states]
        return dahais
    

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


start = time.time()

w = Worker()
learner = Player()
opponent = Player()
w.run_games(learner, opponent, 16)

elapsed_time = time.time() - start
print ("実行時間:{0}".format(elapsed_time) + "[sec]")