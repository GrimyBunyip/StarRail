from baseClasses.BaseCharacter import BaseCharacter
from baseClasses.RelicSet import RelicSet
from baseClasses.BuffEffect import BuffEffect

class BelobogOfTheArchitects(RelicSet):
    def __init__(self,
                graphic:str='',
                shortname:str='Belobog of the Architects',
                uptime:float = 1.0,
                **config):
        self.graphic = graphic
        self.shortname = shortname
        self.uptime = uptime

    def equipTo(self, char:BaseCharacter):
        char.addStat('DEF.percent',description=self.shortname,
                                amount=0.15)
        char.addStat('DEF.percent',description=self.shortname,
                                amount=0.15,
                                uptime=self.uptime)