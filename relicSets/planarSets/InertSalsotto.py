from baseClasses.BaseCharacter import BaseCharacter
from baseClasses.RelicSet import RelicSet
from baseClasses.BuffEffect import BuffEffect

class InertSalsotto(RelicSet):
    def __init__(self,
                graphic:str='',
                shortname:str='Inert Salsotto',
                uptime:float = 1.0,
                **config):
        self.graphic = graphic
        self.shortname = shortname
        self.uptime = uptime

    def equipTo(self, char:BaseCharacter):
        char.stats['CR'].append(BuffEffect(description=self.shortname,
                                amount=0.08))
        char.stats['DMG'].append(BuffEffect(description=self.shortname,
                                amount=0.15,
                                type='ultimate',
                                uptime=self.uptime))
        char.stats['DMG'].append(BuffEffect(description=self.shortname,
                                amount=0.15,
                                type='followup',
                                uptime=self.uptime))