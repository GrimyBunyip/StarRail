from baseClasses.BaseCharacter import BaseCharacter
from baseClasses.RelicSet import RelicSet

class MusketeerOfWildWheat2pc(RelicSet):
    def __init__(self,
                graphic:str='',
                shortname:str='Wildwheat 2pc',
                **config):
        self.graphic = graphic
        self.shortname = shortname

    def equipTo(self, char:BaseCharacter):
        char.addStat('ATK.percent',description=self.shortname,
                                amount=0.12)

class MusketeerOfWildWheat4pc(RelicSet):
    def __init__(self,
                graphic:str='',
                shortname:str='Wildwheat 4pc',
                **config):
        self.graphic = graphic
        self.shortname = shortname

    def equipTo(self, char:BaseCharacter):
        char.addStat('SPD.percent',description=self.shortname,
                                amount=0.06)
        char.addStat('DMG',description=self.shortname,
                                amount=0.10,
                                type=['basic'])