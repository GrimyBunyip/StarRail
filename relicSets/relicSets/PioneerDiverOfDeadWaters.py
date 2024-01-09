from baseClasses.BaseCharacter import BaseCharacter
from baseClasses.RelicSet import RelicSet

class Pioneer2pc(RelicSet):
    def __init__(self,
                graphic:str='',
                shortname:str='Pioneer 2pc',
                uptime:float=1.0,
                **config):
        self.graphic = graphic
        self.shortname = shortname
        self.uptime=uptime

    def equipTo(self, char:BaseCharacter):
        char.addStat('DMG',description=self.shortname,amount=0.12,uptime=self.uptime)
        
class Pioneer4pc(RelicSet):
    def __init__(self,
                graphic:str='',
                shortname:str='Pioneer 4pc',
                stacks:int = 3,
                doubleUptime:float=1.0,
                **config):
        self.graphic = graphic
        self.shortname = shortname
        self.stacks = min(3,stacks)
        self.doubleUptime = doubleUptime

    def equipTo(self, char:BaseCharacter):
        char.addStat('CR',description=self.shortname,amount=0.04,stacks=1.0+self.doubleUptime)
        if self.stacks >= 3:
            char.addStat('CD',description=self.shortname,amount=0.12,stacks=1.0+self.doubleUptime)
        elif self.stacks == 2:
            char.addStat('CD',description=self.shortname,amount=0.08,stacks=1.0+self.doubleUptime)
