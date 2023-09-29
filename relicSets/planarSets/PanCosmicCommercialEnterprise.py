from baseClasses.BaseCharacter import BaseCharacter
from baseClasses.RelicSet import RelicSet
from baseClasses.BuffEffect import BuffEffect

class PanCosmicCommercialEnterprise(RelicSet):
    def __init__(self,
                graphic:str='',
                shortname:str='Pan-Cosmic Commercial Enterprise',
                **config):
        self.graphic = graphic
        self.shortname = shortname

    def equipTo(self, char:BaseCharacter):
        char.addStat('EHR',description=self.shortname,
                                amount=0.1)
        char.addStat('ATK.percent',description=self.shortname,
                                amount=min(0.25, char.getTotalStat('EHR') * 0.25)) # be wary of sequencing issues, equipping gear is usually done last fortunately