from baseClasses.BaseCharacter import BaseCharacter
from baseClasses.RelicSet import RelicSet
from baseClasses.BuffEffect import BuffEffect

class PasserbyOfWanderingCloud2pc(RelicSet):
    def __init__(self,
                graphic:str='',
                shortname:str='Passerby 2pc',
                **config):
        self.graphic = graphic
        self.shortname = shortname

    def equipTo(self, char:BaseCharacter):
        char.Heal += 0.10