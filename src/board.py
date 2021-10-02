from dataclasses import dataclass, field
import random
from player import Player
import time

@dataclass
class Board:
    player_list: list = field(default_factory=list)
    bakaze: int = 0
    kyoku_num: int = 0
    dora_makers: str = ''
    wall_tiles: list = field(default_factory=list)
    teban: int = 0

    def start(self):
        """
        局を開始する
        """
        self.__init_wall_tiles()

        INIT_TEHAI_NUM = 13
        self.player_list[0].start(self.wall_tiles[0:INIT_TEHAI_NUM])
        self.player_list[1].start(self.wall_tiles[INIT_TEHAI_NUM:INIT_TEHAI_NUM * 2])
        self.player_list[2].start(self.wall_tiles[INIT_TEHAI_NUM * 2:INIT_TEHAI_NUM * 3])
        self.player_list[3].start(self.wall_tiles[INIT_TEHAI_NUM * 3:INIT_TEHAI_NUM * 4])
        self.wall_tiles = self.wall_tiles[INIT_TEHAI_NUM * 4:]

        print(self.player_list[1].tehai)
        pass
    def __init_wall_tiles(self):
        """
        山を初期化する
        """
        pass
        self.wall_tiles = HAI_LIST * 4
        random.shuffle(self.wall_tiles)
        print('初期山', self.wall_tiles)
    
    def game(self):
        print('game開始')
        self.start()
        for i in range(70):
            player = self.player_list[self.teban]
            tsumo_hai = self.wall_tiles.pop(0)
            dahai = player.turn(tsumo_hai)
            print('プレイヤー', self.teban, '打牌', dahai)

            # 次の手番にする
            self.teban = (self.teban + 1 + 4) % 4
        print('game終了')

HAI_LIST = ['1m', '2m', '3m', '4m', '5m', '6m', '7m', '8m', '9m',
'1p', '2p', '3p', '4p', '5p', '6p', '7p', '8p', '9p',
'1s', '2s', '3s', '4s', '5s', '6s', '7s', '8s', '9s',
'1z', '2z', '3z', '4z', '5z', '6z', '7z']

HAI_LIST_RED = HAI_LIST + ['0m', '0p', '0s']

board = Board(player_list=[Player(), Player(), Player(), Player()])

start = time.time()
board.game()
print(board.wall_tiles)
elapsed_time = time.time() - start
print ("実行時間:{0}".format(elapsed_time) + "[sec]")