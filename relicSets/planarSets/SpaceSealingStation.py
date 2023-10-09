from baseClasses.BaseCharacter import BaseCharacter
from baseClasses.RelicSet import RelicSet

class SpaceSealingStation(RelicSet):
    def __init__(self,
                graphic:str='https://static.wikia.nocookie.net/houkai-star-rail/images/7/78/Item_Space_Sealing_Station.png',
                shortname:str='Space Sealing',
                uptime:float = 1.0,
                **config):
        self.graphic = graphic
        self.shortname = shortname
        self.uptime = uptime

    def equipTo(self, char:BaseCharacter):
        char.addStat('ATK.percent',description=self.shortname,
                                amount=0.12)
        char.addStat('ATK.percent',description=self.shortname,
                                amount=0.12,
                                uptime=self.uptime)