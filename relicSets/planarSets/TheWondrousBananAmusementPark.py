from baseClasses.BaseCharacter import BaseCharacter
from baseClasses.RelicSet import RelicSet

class TheWondrousBananAmusementPark(RelicSet):
    def __init__(self,
                graphic:str='',
                shortname:str='BananA',
                uptime:float = 1.0,
                **config):
        self.graphic = graphic
        self.shortname = shortname
        self.uptime = uptime

    def equipTo(self, char:BaseCharacter):
        char.addStat('CD',description=self.shortname,
                                amount=0.16,)
        char.addStat('CD',description=self.shortname,
                                amount=0.32,
                                uptime=self.uptime)
