from baseClasses.BaseCharacter import BaseCharacter
from baseClasses.RelicSet import RelicSet

class CelestialDifferentiator(RelicSet):
    def __init__(self,
                graphic:str='',
                shortname:str='Celestial Differentiator',
                uptime:float = 0.0,
                **config):
        self.graphic = graphic
        self.shortname = shortname
        self.uptime = uptime

    def equipTo(self, char:BaseCharacter):
        char.addStat('CD',description=self.shortname,
                                amount=0.16)
        char.addStat('CR',description=self.shortname,
                                amount=0.60,
                                uptime=self.uptime)