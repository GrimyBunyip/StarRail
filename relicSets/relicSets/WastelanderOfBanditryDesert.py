from baseClasses.BaseCharacter import BaseCharacter
from baseClasses.RelicSet import RelicSet
from baseClasses.BuffEffect import BuffEffect

class WastelanderOfBanditryDesert2pc(RelicSet):
    def __init__(self,
                graphic:str='',
                shortname:str = 'Wastelander 2pc',
                **config):
        self.graphic = graphic
        self.shortname = shortname

    def equipTo(self, char:BaseCharacter):
        char.addStat('DMG',description=self.shortname,
                                amount=0.10,
                                type='imaginary')
        
class WastelanderOfBanditryDesert4pc(RelicSet):
    def __init__(self,
                graphic:str='',
                shortname:str = 'Wastelander 4pc',
                uptimeCR:float = 1.0,
                uptimeCD:float = 0.25,
                **config):
        self.graphic = graphic
        self.shortname = shortname
        self.uptimeCR = uptimeCR
        self.uptimeCD = uptimeCD

    def equipTo(self, char:BaseCharacter):
        char.addStat('CR',description=self.shortname,
                                amount=0.10,
                                uptime=self.uptimeCR)
        char.addStat('CD',description=self.shortname,
                                amount=0.20,
                                uptime=self.uptimeCD)