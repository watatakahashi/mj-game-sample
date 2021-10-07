from dataclasses import dataclass
import random
from board import Board
# import time
from predict import Predictor
import pandas as pd


@dataclass
class Player:
    clf = Predictor()

    def get_dahai(self, states: Board):
        if len(states) == 0:
            return []
        # 打牌を決定する、手牌からは取り除かない
        records = pd.DataFrame()
        for state in states:
            records = records.append(state.generate_state_record())

        # start = time.time()

        max_indexes = self.clf.multi_predict(records)

        # elapsed_time = time.time() - start
        # print ("予測実行時間:{0}".format(elapsed_time) + "[sec]")

        dahais = [HAI_TYPES[i] for i in max_indexes]

        # 手牌になければランダム
        select_dahais = []
        for state, dahai in zip(states, dahais):
            tehai = state.private_tiles[state.tsumo_player]
            select_dahais += [
                dahai if dahai in tehai else random.choice(tehai)]
            # print(modules.utils.sort_tehai(tehai), dahai)
        return select_dahais


HAI_TYPES = ['0m', '1m', '2m', '3m', '4m', '5m', '6m', '7m', '8m', '9m',
             '0p', '1p', '2p', '3p', '4p', '5p', '6p', '7p', '8p', '9p',
             '0s', '1s', '2s', '3s', '4s', '5s', '6s', '7s', '8s', '9s',
             '1z', '2z', '3z', '4z', '5z', '6z', '7z']


@dataclass
class RandomPlayer:

    def get_dahai(self, states):
        if len(states) == 0:
            return []
        dahais = [random.choice(state.private_tiles[state.tsumo_player])
                  for state in states]
        return dahais
