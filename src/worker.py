from player import Player
import argparse
from dataclasses import dataclass
from board import Board
import time
import random


@dataclass
class Worker:

    def run_games(self, learner, opponent, num_games=1, seed=0):
        random.seed(seed)

        idxs_to_unfinished_states = {
            i: Board(
                learner=(
                    i + 4) %
                4) for i in range(num_games)}

        # 東1局を開始する
        [state.start_kyoku() for state in idxs_to_unfinished_states.values()]

        while len(idxs_to_unfinished_states) > 0:
            # for i in range(500):
            # print('順目', i)

            # 自分のツモ番
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

            # 自分以外のツモ番
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

            # 手番の更新とツモ、ツモ和了確認まで行う
            just_finished = []
            for key, state in idxs_to_unfinished_states.items():
                # state.__next_player()
                # state.tsumo()
                if state.is_end_of_game:
                    just_finished += [key]
            # ゲームが終了していたらstatesから除外する
            for idx in just_finished:
                del idxs_to_unfinished_states[idx]


parser = argparse.ArgumentParser(description='麻雀の自己対戦')
parser.add_argument('-c', '--count', default=4, help='試合数')
parser.add_argument('-s', '--seed', default=0, help='乱数シード値')
args = parser.parse_args()

num_games: int = args.count
seed: int = args.seed

w = Worker()

learner = Player()
opponent = Player()

start = time.time()

w.run_games(learner, opponent, int(num_games), int(seed))

elapsed_time = time.time() - start
print("実行時間:{0}".format(elapsed_time) + "[sec]")
