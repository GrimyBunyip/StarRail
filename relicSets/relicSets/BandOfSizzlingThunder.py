from baseClasses.BaseCharacter import BaseCharacter
from baseClasses.RelicSet import RelicSet

class BandOfSizzlingThunder2pc(RelicSet):
    def __init__(self,
                graphic:str='',
                shortname:str = 'Band 2pc',
                **config):
        self.graphic = graphic
        self.shortname = shortname

    def equipTo(self, char:BaseCharacter):
        char.lighDmg += 0.10
        
class BandOfSizzlingThunder4pc(RelicSet):
    def __init__(self,
                graphic:str='',
                shortname:str = 'Band 4pc',
                uptime:float = 1.0,
                **config):
        self.graphic = graphic
        self.shortname = shortname
        self.uptime = uptime

    def equipTo(self, char:BaseCharacter):
        char.percAtk += 0.20 * self.uptime