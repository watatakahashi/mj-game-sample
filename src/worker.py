from dataclasses import dataclass, field
from board import Board
from player import Player, RandomPlayer
import random
import time
import numpy as np
import pandas as pd
import sys

@dataclass
class Worker:

    def run_games(self, learner, opponent, num_games=1):
        idxs_to_unfinished_states = {i: Board(learner=(i + 4) % 4) for i in range(num_games)}

        # 東1局を開始する
        [state.start_kyoku() for state in idxs_to_unfinished_states.values()]

        # while len(idxs_to_unfinished_states) > 0:
        for i in range(70):
            print('順目', i)

            # 自分のツモ番
            learner_states = list(filter(lambda state: state.tsumo_player == state.learner, idxs_to_unfinished_states.values()))
            dahais = learner.get_dahai(learner_states)

            # 状態の更新
            for state, dahai in zip(learner_states, dahais):
                state.dahai(dahai)
                pass
                # TODO: 打牌に対するアクション
            
            # 自分以外のツモ番
            not_learner_state = list(filter(lambda state: state.tsumo_player != state.learner, idxs_to_unfinished_states.values()))
            dahais = opponent.get_dahai(not_learner_state)
            
            # 状態の更新
            for state, dahai in zip(not_learner_state, dahais):
                state.dahai(dahai)
                pass
                # TODO: 打牌に対するアクション

            # 手番の更新とツモ、ツモ和了確認まで行う
            just_finished = []
            for key, state in idxs_to_unfinished_states.items():
                state.next_player()
                state.tsumo()
                if state.is_end_of_game:
                    just_finished += [key]
            # ゲームが終了していたらstatesから除外する
            for idx in just_finished:
                del idxs_to_unfinished_states[idx]

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

w = Worker()
learner = Player()
opponent = Player()

num_games = int(sys.argv[1]) if sys.argv[1] is not None else 4

start = time.time()

w.run_games(learner, opponent, num_games)

elapsed_time = time.time() - start
print ("実行時間:{0}".format(elapsed_time) + "[sec]")