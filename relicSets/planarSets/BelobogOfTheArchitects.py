from baseClasses.BaseCharacter import BaseCharacter
from baseClasses.RelicSet import RelicSet

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
        char.percDef += 0.15
        char.percDef += 0.15 * self.uptime