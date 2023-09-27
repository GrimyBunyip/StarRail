from baseClasses.BaseCharacter import BaseCharacter
from baseClasses.RelicSet import RelicSet

class ThiefOfShootingMeteor2pc(RelicSet):
    def __init__(self,
                graphic:str='',
                shortname:str = 'Thief 2pc',
                **config):
        self.graphic = graphic
        self.shortname = shortname

    def equipTo(self, char:BaseCharacter):
        char.breakEffect += 0.16
        
class ThiefOfShootingMeteor4pc(RelicSet):
    def __init__(self,
                graphic:str='',
                shortname:str = 'Thief 4pc',
                uptime:float = 1.0,
                **config):
        self.graphic = graphic
        self.shortname = shortname
        self.uptime = uptime

    def equipTo(self, char:BaseCharacter):
        char.breakEffect += 0.16
        # energy mechanics not really implemented