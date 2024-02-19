from baseClasses.BaseCharacter import BaseCharacter
from baseClasses.RelicSet import RelicSet

class SigoniaTheUnclaimedDesolation(RelicSet):
    def __init__(self,
                graphic:str='',
                shortname:str='Sigonia',
                stacks:float = 10.0,
                **config):
        self.graphic = graphic
        self.shortname = shortname
        self.stacks = stacks

    def equipTo(self, char:BaseCharacter):
        char.addStat('CD',description=self.shortname,
                                amount=0.04,
                                stacks=self.stacks)