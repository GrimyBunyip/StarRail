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
        char.CR += 0.08
        char.DmgType['ultimate'] += 0.15 * self.uptime
        char.DmgType['followup'] += 0.15 * self.uptime