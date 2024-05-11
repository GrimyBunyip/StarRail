from baseClasses.BaseCharacter import BaseCharacter
from baseClasses.RelicSet import RelicSet

class ForgeOfTheKalpagniLantern(RelicSet):
    def __init__(self,
                graphic:str='',
                shortname:str='Kalpagni',
                uptime:float = 1.0,
                **config):
        self.graphic = graphic
        self.shortname = shortname
        self.uptime = uptime

    def equipTo(self, char:BaseCharacter):
        char.addStat('SPD.percent',description=self.shortname,
                                amount=0.06)
        char.addStat('CD',description=self.shortname,
                                amount=0.40,
                                uptime=self.uptime)
        # party wide buffs not yet implemented