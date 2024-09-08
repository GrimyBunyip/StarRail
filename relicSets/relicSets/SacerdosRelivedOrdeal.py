from baseClasses.BaseCharacter import BaseCharacter
from baseClasses.RelicSet import RelicSet

class SacerdosRelivedOrdeal2pc(RelicSet):
    def __init__(self,
                graphic:str='',
                shortname:str='Sacerdos 2pc',
                **config):
        self.graphic = graphic
        self.shortname = shortname

    def equipTo(self, char:BaseCharacter):
        char.addStat('SPD.percent',description=self.shortname,
                                amount=0.06)
        
class SacerdosRelivedOrdeal4pc(RelicSet):
    def __init__(self,
                graphic:str='',
                shortname:str='Sacerdos 4pc',
                uptime = 0.2,
                **config):
        self.graphic = graphic
        self.shortname = shortname
        self.uptime = uptime

    def equipTo(self, char:BaseCharacter):
        pass
        # implement manually