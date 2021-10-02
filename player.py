from dataclasses import dataclass, field
import random

@dataclass
class Player:
    tehai: list = field(default_factory=list)

    def start(self, tehai):
        self.tehai = tehai

    def turn(self, tsumo_hai):
        self.__tsumo(tsumo_hai)
        dahai = self.__dahai()
        return dahai
    def __tsumo(self, hai):
        self.tehai += [hai]
    
    def __dahai(self):
        dahai = random.choice(self.tehai)
        self.tehai.remove(dahai)
        return dahai

# p = Player()
# p.start(['1m', '2m', '3m', '4m'])
# dahai = p.turn('5m')
# print(p.tehai, dahai)