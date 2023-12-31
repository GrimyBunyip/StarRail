from baseClasses.BaseCharacter import BaseCharacter
from baseClasses.RelicSet import RelicSet
from baseClasses.BuffEffect import BuffEffect

class MessengerTraversingHackerspace2pc(RelicSet):
    def __init__(self,
                graphic:str='',
                shortname:str='Messenger 2pc',
                **config):
        self.graphic = graphic
        self.shortname = shortname

    def equipTo(self, char:BaseCharacter):
        char.addStat('SPD.percent',description=self.shortname,
                                amount=0.06)
        
class MessengerTraversingHackerspace4pc(RelicSet):
    def __init__(self,
                graphic:str='',
                shortname:str='Messenger 4pc',
                uptime = 1.0/3.0,
                **config):
        self.graphic = graphic
        self.shortname = shortname
        self.uptime = uptime

    def equipTo(self, char:BaseCharacter):
        char.addStat('SPD.percent',description=self.shortname,
                                amount=0.12,
                                uptime=self.uptime)