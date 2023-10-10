from baseClasses.BaseCharacter import BaseCharacter
from baseClasses.RelicSet import RelicSet

class GrandDuke2pc(RelicSet):
    def __init__(self,
                graphic:str='',
                shortname:str='Grand Duke 2pc',
                **config):
        self.graphic = graphic
        self.shortname = shortname

    def equipTo(self, char:BaseCharacter):
        char.addStat('DMG',description=self.shortname,
                                amount=0.16,type=['followup'])
        
class GrandDuke4pc(RelicSet):
    def __init__(self,
                graphic:str='',
                shortname:str='Grand Duke 4pc',
                stacks = 4.0,
                **config):
        self.graphic = graphic
        self.shortname = shortname
        self.stacks = min(8.0,stacks)

    def equipTo(self, char:BaseCharacter):
        char.addStat('DMG',description=self.shortname,
                                amount=0.08,stacks=self.stacks,type=['followup'])