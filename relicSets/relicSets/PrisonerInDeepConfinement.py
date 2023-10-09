from baseClasses.BaseCharacter import BaseCharacter
from baseClasses.RelicSet import RelicSet

class Prisoner2pc(RelicSet):
    def __init__(self,
                graphic:str='',
                shortname:str='Prisoner 2pc',
                **config):
        self.graphic = graphic
        self.shortname = shortname

    def equipTo(self, char:BaseCharacter):
        char.addStat('ATK.percent',description=self.shortname,amount=0.12)
        
class Prisoner4pc(RelicSet):
    def __init__(self,
                graphic:str='',
                shortname:str='Prisoner 4pc',
                stacks = 3.0,
                **config):
        self.graphic = graphic
        self.shortname = shortname
        self.stacks = min(3.0,stacks)

    def equipTo(self, char:BaseCharacter):
        char.addStat('DefShred',description=self.shortname,
                                amount=0.06,stacks=self.stacks)