from baseClasses.BaseCharacter import BaseCharacter
from baseClasses.RelicSet import RelicSet
from baseClasses.BuffEffect import BuffEffect

class GuardOfWutheringSnow2pc(RelicSet):
    def __init__(self,
                graphic:str='',
                shortname:str='Guard 2pc',
                **config):
        self.graphic = graphic
        self.shortname = shortname

    def equipTo(self, char:BaseCharacter):
        char.dmgReduction += 0.08