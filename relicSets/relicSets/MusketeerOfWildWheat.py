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
        char.stats['ATK'].append(BuffEffect(description=self.shortname,
                                amount=0.12,
                                mathType='percent'))

class MusketeerOfWildWheat4pc(RelicSet):
    def __init__(self,
                graphic:str='',
                shortname:str='Wildwheat 4pc',
                **config):
        self.graphic = graphic
        self.shortname = shortname

    def equipTo(self, char:BaseCharacter):
        char.stats['SPD'].append(BuffEffect(description=self.shortname,
                                amount=0.06,
                                mathType='percent'))
        char.stats['DMG'].append(BuffEffect(description=self.shortname,
                                amount=0.10,
                                type='basic'))