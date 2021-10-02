from dataclasses import dataclass, field
import random
import numpy as np
import pandas as pd
from predict import Predictor


@dataclass
class Player:
    tehai: list = field(default_factory=list)
    clf = Predictor()

    def start(self, tehai):
        self.tehai = tehai

    def turn(self, tsumo_hai):
        self.__tsumo(tsumo_hai)
        dahai = self.__dahai()
        return dahai
    def __tsumo(self, hai):
        self.tehai += [hai]
    
    def __dahai(self):
        df = self.__create_predict_data()
        pre, prob_list = self.clf.predict(df)

        dahai = random.choice(self.tehai)
        self.tehai.remove(dahai)
        return dahai
    def __create_predict_data(self):
        df = pd.DataFrame([[
            0,
            ''.join(self.tehai),
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

# p = Player()
# p.start(['1m', '2m', '3m', '4m'])
# dahai = p.turn('5m')
# print(p.tehai, dahai)