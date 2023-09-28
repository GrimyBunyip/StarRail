from baseClasses.BaseCharacter import BaseCharacter
from baseClasses.RelicSet import RelicSet
from baseClasses.BuffEffect import BuffEffect

class LongevousDisciple2pc(RelicSet):
    def __init__(self,
                graphic:str='',
                shortname:str='Longevous 2pc',
                **config):
        self.graphic = graphic
        self.shortname = shortname

    def equipTo(self, char:BaseCharacter):
        char.addStat('HP',description=self.shortname,
                                amount=0.12,
                                mathType='percent')
        
class LongevousDisciple4pc(RelicSet):
    def __init__(self,
                graphic:str='',
                shortname:str='Longevous 4pc',
                uptime = 1.0,
                **config):
        self.graphic = graphic
        self.shortname = shortname
        self.uptime = uptime

    def equipTo(self, char:BaseCharacter):
        char.addStat('CR',description=self.shortname,
                                amount=0.16,
                                uptime=self.uptime)