from baseClasses.BaseCharacter import BaseCharacter
from baseClasses.RelicSet import RelicSet
from baseClasses.BuffEffect import BuffEffect

class MusketeerOfWildWheat2pc(RelicSet):
    def __init__(self,
                graphic:str='',
                shortname:str='Wildwheat 2pc',
                **config):
        self.graphic = graphic
        self.shortname = shortname

    def equipTo(self, char:BaseCharacter):
        char.percAtk += 0.12

class MusketeerOfWildWheat4pc(RelicSet):
    def __init__(self,
                graphic:str='',
                shortname:str='Wildwheat 4pc',
                **config):
        self.graphic = graphic
        self.shortname = shortname

    def equipTo(self, char:BaseCharacter):
        char.percSpd += 0.06
        char.DmgType['basic'] += 0.10