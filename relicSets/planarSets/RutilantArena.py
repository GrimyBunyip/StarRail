from baseClasses.BaseCharacter import BaseCharacter
from baseClasses.RelicSet import RelicSet
from baseClasses.BuffEffect import BuffEffect

class RutilantArena(RelicSet):
    def __init__(self,
                graphic:str='',
                shortname:str='Rutilant Arena',
                uptime:float=1.0,
                **config):
        self.graphic = graphic
        self.shortname = shortname
        self.uptime = uptime

    def equipTo(self, char:BaseCharacter):
        char.addStat('CR',description=self.shortname,
                                amount=0.08)
        char.addStat('DMG',description=self.shortname,
                                amount=0.20,
                                type=['basic'],
                                uptime=self.uptime)
        char.addStat('DMG',description=self.shortname,
                                amount=0.20,
                                type=['skill'],
                                uptime=self.uptime)