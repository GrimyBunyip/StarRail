from baseClasses.BaseCharacter import BaseCharacter
from baseClasses.RelicSet import RelicSet
from baseClasses.BuffEffect import BuffEffect

class SprightlyVonwacq(RelicSet):
    def __init__(self,
                graphic:str='',
                shortname:str='Sprightly Vonwacq',
                **config):
        self.graphic = graphic
        self.shortname = shortname

    def equipTo(self, char:BaseCharacter):
        char.stats['ER'].append(BuffEffect(description=self.shortname,
                                amount=0.05))
        # second effect not implemented