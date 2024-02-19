from baseClasses.BaseCharacter import BaseCharacter
from baseClasses.RelicSet import RelicSet

class IzumoGenseiAndTakamaDivineRealm(RelicSet):
    def __init__(self,
                graphic:str='',
                shortname:str='Izumo',
                **config):
        self.graphic = graphic
        self.shortname = shortname

    def equipTo(self, char:BaseCharacter):
        char.addStat('ATK.percent',description=self.shortname,amount=0.12)
        char.addStat('CR',description=self.shortname,amount=0.12)