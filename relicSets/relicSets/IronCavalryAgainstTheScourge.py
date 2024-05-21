from baseClasses.BaseCharacter import BaseCharacter
from baseClasses.RelicSet import RelicSet

class IronCavalryAgainstTheScourge2pc(RelicSet):
    def __init__(self,
                graphic:str='',
                shortname:str = 'Iron Cavalry 2pc',
                **config):
        self.graphic = graphic
        self.shortname = shortname

    def equipTo(self, char:BaseCharacter):
        char.addStat('BreakEffect',description=self.shortname,
                                        amount=0.16)
        
class IronCavalryAgainstTheScourge4pc(RelicSet):
    def __init__(self,
                graphic:str='',
                shortname:str = 'Iron Cavalry 4pc',
                breakEffect:float=2.5,
                **config):
        self.graphic = graphic
        self.shortname = shortname
        self.breakEffect = breakEffect

    def equipTo(self, char:BaseCharacter):
        char.addStat('DefShred',description=self.shortname,
                                        amount=0.10 if self.breakEffect >= 1.5 else 0.0,
                                        type=['break'])
        char.addStat('DefShred',description=self.shortname,
                                        amount=0.15 if self.breakEffect >= 2.5 else 0.0,
                                        type=['superBreak'])
