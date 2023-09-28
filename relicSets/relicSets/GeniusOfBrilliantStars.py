from baseClasses.BaseCharacter import BaseCharacter
from baseClasses.RelicSet import RelicSet
from baseClasses.BuffEffect import BuffEffect

class GeniusOfBrilliantStars2pc(RelicSet):
    def __init__(self,
                graphic:str='',
                shortname:str = 'Genius 2pc',
                **config):
        self.graphic = graphic
        self.shortname = shortname

    def equipTo(self, char:BaseCharacter):
        char.addStat('DMG',description=self.shortname,
                                amount=0.10,
                                type='quantum')
        
class GeniusOfBrilliantStars4pc(RelicSet):
    def __init__(self,
                graphic:str='',
                shortname:str = 'Genius 4pc',
                uptime:float = 1.0,
                **config):
        self.graphic = graphic
        self.shortname = shortname
        self.uptime = uptime

    def equipTo(self, char:BaseCharacter):
        char.addStat('DefShred',description=self.shortname,
                                    amount=0.10)
        char.addStat('DefShred',description=self.shortname,
                                    amount=0.10,
                                    uptime=self.uptime)