import argparse
import random
import time
from dataclasses import dataclass
from typing import Dict

from board import Board
from player import Player, PolicyPlayer
import pandas as pd
import os

RESULT_FILE_PATH = 'data/sample.csv'

if os.path.isfile(RESULT_FILE_PATH):
    os.remove(RESULT_FILE_PATH)


@dataclass
class Worker:

    def run_games(
            self,
            learner: Player,
            opponent: Player,
            num_games=1,
            seed=0):
        random.seed(seed)

        idxs_to_unfinished_states = {
            i: Board(
                learner=(
                    i + 4) %
                4) for i in range(num_games)}

        while len(idxs_to_unfinished_states) > 0:

            # 自分の打牌
            learner_states = list(
                filter(
                    lambda state: state.tsumo_player == state.learner,
                    idxs_to_unfinished_states.values()))
            dahais = learner.get_dahai(learner_states)

            # 状態の更新
            for state, dahai in zip(learner_states, dahais):
                state.dahai(dahai)
                pass
                # TODO: 打牌に対するアクション

            idxs_to_unfinished_states = self.__exclude_end_of_game(
                idxs_to_unfinished_states)

            # 自分以外の打牌
            not_learner_state = list(
                filter(
                    lambda state: state.tsumo_player != state.learner,
                    idxs_to_unfinished_states.values()))
            dahais = opponent.get_dahai(not_learner_state)

            # 状態の更新
            for state, dahai in zip(not_learner_state, dahais):
                state.dahai(dahai)
                pass
                # TODO: 打牌に対するアクション

            idxs_to_unfinished_states = self.__exclude_end_of_game(
                idxs_to_unfinished_states)

            # unfinished_len = len(idxs_to_unfinished_states.values())
            # print(f'残りゲーム数={unfinished_len}')

    def __exclude_end_of_game(self, states: Dict[int, Board]):
        just_finished = []
        for key, state in states.items():
            if state.is_end_of_game:
                just_finished += [key]
                print(f'ゲーム終了 idx={key}')
        for idx in just_finished:
            self.__save_to_csv(
                states[idx].training_data)
            print(states[idx].training_data.shape)
            del states[idx]
        return states

    def __save_to_csv(self, df: pd.DataFrame):
        if os.path.isfile(RESULT_FILE_PATH):
            df.to_csv(RESULT_FILE_PATH, mode='a', header=False, index=False)
        else:
            df.to_csv(RESULT_FILE_PATH, index=False)


parser = argparse.ArgumentParser(description='麻雀の自己対戦')
parser.add_argument('-c', '--count', default=4, help='試合数')
parser.add_argument('-s', '--seed', default=0, help='乱数シード値')
args = parser.parse_args()

num_games: int = args.count
seed: int = args.seed

w = Worker()

learner = PolicyPlayer()
opponent = PolicyPlayer()

start = time.time()

w.run_games(learner, opponent, int(num_games), int(seed))

elapsed_time = time.time() - start
print("実行時間:{0}".format(elapsed_time) + "[sec]")
