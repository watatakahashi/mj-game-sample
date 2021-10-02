from dataclasses import dataclass, field
import random
from player import Player

@dataclass
class Board:
    player_list: list = field(default_factory=list)
    bakaze: int = 0
    kyoku_num: int = 0
    dora_makers: str = ''
    wall_tiles: list = field(default_factory=list)

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
        self.start()
        for i in range(60):
            pass

HAI_LIST = ['1m', '2m', '3m', '4m', '5m', '6m', '7m', '8m', '9m',
'1p', '2p', '3p', '4p', '5p', '6p', '7p', '8p', '9p',
'1s', '2s', '3s', '4s', '5s', '6s', '7s', '8s', '9s',
'1z', '2z', '3z', '4z', '5z', '6z', '7z']

HAI_LIST_RED = HAI_LIST + ['0m', '0p', '0s']

board = Board(player_list=[Player(), Player(), Player(), Player()])
board.game()