from baseClasses.BaseCharacter import BaseCharacter
from baseClasses.RelicSet import RelicSet
from baseClasses.BuffEffect import BuffEffect

class ChampionOfStreetwiseBoxing2pc(RelicSet):
    def __init__(self,
                graphic:str='',
                shortname:str = 'Champion 2pc',
                **config):
        self.graphic = graphic
        self.shortname = shortname

    def equipTo(self, char:BaseCharacter):
        char.addStat('DMG',description=self.shortname,
                                amount=0.10,
                                type='physical')
        
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
        char.addStat('ATK',description=self.shortname,
                                amount=0.05,
                                mathType='percent',
                                stacks=self.stacks)