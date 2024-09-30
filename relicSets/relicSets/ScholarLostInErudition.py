from baseClasses.BaseCharacter import BaseCharacter
from baseClasses.RelicSet import RelicSet

class ScholarLostInErudition2pc(RelicSet):
    def __init__(self,
                graphic:str='',
                shortname:str='Scholar 2pc',
                **config):
        self.graphic = graphic
        self.shortname = shortname

    def equipTo(self, char:BaseCharacter):
        char.addStat('CR',description=self.shortname,amount=0.08)
        
class ScholarLostInErudition4pc(RelicSet):
    def __init__(self,
                graphic:str='',
                shortname:str='Scholar 4pc',
                uptime = 1.0 / 3.0,
                **config):
        self.graphic = graphic
        self.shortname = shortname
        self.uptime = uptime

    def equipTo(self, char:BaseCharacter):
        # buff applied to followup attacks
        char.addStat('DMG',description=self.shortname,amount=0.20, type=['ultimate','skill'])
        char.addStat('DMG',description=self.shortname,
                     amount=0.25,
                     uptime=self.uptime,
                     type=['skill'])