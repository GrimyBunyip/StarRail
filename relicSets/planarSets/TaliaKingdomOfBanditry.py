from baseClasses.BaseCharacter import BaseCharacter
from baseClasses.RelicSet import RelicSet
from baseClasses.BuffEffect import BuffEffect

class TaliaKingdomOfBanditry(RelicSet):
    def __init__(self,
                graphic:str='',
                shortname:str='Talia: Kingdom of Banditry',
                uptime:float = 1.0,
                **config):
        self.graphic = graphic
        self.shortname = shortname
        self.uptime = uptime

    def equipTo(self, char:BaseCharacter):
        char.stats['BreakEffect'].append(BuffEffect(description=self.shortname,
                                        amount=0.16))
        char.stats['BreakEffect'].append(BuffEffect(description=self.shortname,
                                        amount=0.2,
                                        uptime=self.uptime))