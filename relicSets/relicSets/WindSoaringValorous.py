from baseClasses.BaseCharacter import BaseCharacter
from baseClasses.RelicSet import RelicSet

class WindSoaringValorous2pc(RelicSet):
    def __init__(self,
                graphic:str='',
                shortname:str='Wind Soaring 2pc',
                **config):
        self.graphic = graphic
        self.shortname = shortname

    def equipTo(self, char:BaseCharacter):
        char.addStat('ATK.percent',description=self.shortname,amount=0.12)
        
class WindSoaringValorous4pc(RelicSet):
    def __init__(self,
                graphic:str='',
                shortname:str='Wind Soaring 4pc',
                uptime = 1.0,
                **config):
        self.graphic = graphic
        self.shortname = shortname
        self.uptime = uptime

    def equipTo(self, char:BaseCharacter):
        # buff applied to followup attacks
        char.addStat('CR',description=self.shortname,amount=0.06)
        char.addStat('DMG',description=self.shortname,
                     amount=0.36,
                     uptime=self.uptime,
                     type=['ultimate'])