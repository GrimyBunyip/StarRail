from baseClasses.BaseCharacter import BaseCharacter
from baseClasses.RelicSet import RelicSet

class ChampionOfStreetwiseBoxing2pc(RelicSet):
    def __init__(self,
                graphic:str='',
                shortname:str = 'Champion 2pc',
                **config):
        self.graphic = graphic
        self.shortname = shortname

    def equipTo(self, char:BaseCharacter):
        char.physDmg += 0.10
        
class ChampionOfStreetwiseBoxing4pc(RelicSet):
    def __init__(self,
                graphic:str='',
                shortname:str = 'Champion 4pc',
                stacks:int = 5,
                **config):
        self.graphic = graphic
        self.shortname = shortname
        self.stacks = stacks

    def equipTo(self, char:BaseCharacter):
        char.percAtk += 0.05 * self.stacks