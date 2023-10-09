from baseClasses.BaseCharacter import BaseCharacter
from baseClasses.RelicSet import RelicSet

class KnightOfPurityPalace2pc(RelicSet):
    def __init__(self,
                graphic:str='',
                shortname:str='Knight 2pc',
                **config):
        self.graphic = graphic
        self.shortname = shortname

    def equipTo(self, char:BaseCharacter):
        char.addStat('DEF.percent',description=self.shortname,
                                amount=0.15)

class KnightOfPurityPalace4pc(RelicSet):
    def __init__(self,
                graphic:str='',
                shortname:str='Knight 4pc',
                **config):
        self.graphic = graphic
        self.shortname = shortname

    def equipTo(self, char:BaseCharacter):
        char.addStat('Shield.percent',description=self.shortname,
                                    amount=0.20)