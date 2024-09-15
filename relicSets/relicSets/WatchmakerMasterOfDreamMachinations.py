from baseClasses.BaseCharacter import BaseCharacter
from baseClasses.RelicSet import RelicSet

class Watchmaker2pc(RelicSet):
    def __init__(self,
                graphic:str='',
                shortname:str = 'Watchmaker 2pc',
                **config):
        self.graphic = graphic
        self.shortname = shortname

    def equipTo(self, char:BaseCharacter):
        char.addStat('BreakEffect',description=self.shortname,
                                        amount=0.16)
        
class Watchmaker4pc(RelicSet):
    def __init__(self,
                graphic:str='',
                shortname:str = 'Watchmaker 4pc',
                uptime:float = 0.66,
                **config):
        self.graphic = graphic
        self.shortname = shortname
        self.uptime = uptime

    def equipTo(self, char:BaseCharacter):
        char.addStat('BreakEffect',description=self.shortname,
                                        amount=0.30,
                                        uptime=self.uptime)