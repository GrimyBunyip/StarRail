from baseClasses.BaseCharacter import BaseCharacter
from baseClasses.RelicSet import RelicSet

class InertSalsotto(RelicSet):
    def __init__(self,
                graphic:str='',
                shortname:str='Inert Salsotto',
                uptime:float = 1.0,
                **config):
        self.graphic = graphic
        self.shortname = shortname
        self.uptime = uptime

    def equipTo(self, char:BaseCharacter):
        char.addStat('CR',description=self.shortname,
                                amount=0.08)
        char.addStat('DMG',description=self.shortname,
                                amount=0.15,
                                type=['ultimate','followup'],
                                uptime=self.uptime)
