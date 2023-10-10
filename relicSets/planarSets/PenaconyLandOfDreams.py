from baseClasses.BaseCharacter import BaseCharacter
from baseClasses.RelicSet import RelicSet

class PenaconyLandOfDreams(RelicSet):
    def __init__(self,
                graphic:str='',
                shortname:str='Penacony',
                **config):
        self.graphic = graphic
        self.shortname = shortname

    def equipTo(self, char:BaseCharacter):
        char.addStat('ER',description=self.shortname,
                                amount=0.05)
        char.addStat('DMG',description=self.shortname,
                                amount=0.10)