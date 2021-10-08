from player import Player, PolicyPlayer
import argparse
from dataclasses import dataclass
from board import Board
import time
import random


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

            # ゲームが終了していたらstatesから除外する
            just_finished = []
            for key, state in idxs_to_unfinished_states.items():
                if state.is_end_of_game:
                    just_finished += [key]
                    print(f'ゲーム終了 idx={key}')
            for idx in just_finished:
                del idxs_to_unfinished_states[idx]

            # unfinished_len = len(idxs_to_unfinished_states.values())
            # print(f'残りゲーム数={unfinished_len}')


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
