from dataclasses import dataclass
import random
from typing import List
from board import Board
# import time
from predict import Predictor
import pandas as pd


class Player(object):
    def get_dahai(self, states: Board):
        pass

    def get_reach(self, states: Board):
        pass

    def get_action(self, states: List):
        pass


@dataclass
class PolicyPlayer(Player):
    clf = Predictor()

    def get_dahai(self, states: List[Board]):
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
            if state.is_tsumo_player_reach():
                select_dahais += [dahai]
            else:
                tehai = state.private_tiles[state.tsumo_player]
                if dahai in tehai:
                    select_dahais += [dahai]
                else:
                    rand_dahai = random.choice(tehai)
                    print('非合法手 ', '手牌', tehai, 'ランダム選択:', rand_dahai)
                    select_dahais += [rand_dahai]
            # select_dahais += [
            #     dahai if dahai in tehai else random.choice(tehai)]
            # print(modules.utils.sort_tehai(tehai), dahai)
        return select_dahais

    def get_reach(self, states: List[Board]):
        if len(states) == 0:
            return []

        records = pd.DataFrame()
        for state in states:
            records = records.append(state.generate_reach_state_record())

        # print(
        # f'手牌:{records.privateTehaiString.values}
        # ドラ表示:{records.doraOpen.values}')
        max_indexes = self.clf.predict_reach(records)
        # print(max_indexes)

        select_reaches = list(map(lambda is_reach: is_reach == 1, max_indexes))
        return select_reaches

    def get_action(self, states: List):
        if len(states) == 0:
            return []

        records = pd.DataFrame()
        for state in states:
            records = records.append(
                state['state'].generate_action_state_record(state['player']))
        # print(records)
        max_indexes = self.clf.predict_action(records)
        # print(max_indexes)

        return max_indexes


HAI_TYPES = ['0m', '1m', '2m', '3m', '4m', '5m', '6m', '7m', '8m', '9m',
             '0p', '1p', '2p', '3p', '4p', '5p', '6p', '7p', '8p', '9p',
             '0s', '1s', '2s', '3s', '4s', '5s', '6s', '7s', '8s', '9s',
             '1z', '2z', '3z', '4z', '5z', '6z', '7z']


@dataclass
class RandomPlayer(Player):

    def get_dahai(self, states):
        if len(states) == 0:
            return []
        dahais = [random.choice(state.private_tiles[state.tsumo_player])
                  for state in states]
        return dahais
