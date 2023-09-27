from baseClasses.BaseCharacter import BaseCharacter
from baseClasses.RelicSet import RelicSet

class FiresmithOfLavaForging2pc(RelicSet):
    def __init__(self,
                graphic:str='',
                shortname:str = 'Firesmith 2pc',
                **config):
        self.graphic = graphic
        self.shortname = shortname

    def equipTo(self, char:BaseCharacter):
        char.fireDmg += 0.10
        
class FiresmithOfLavaForging4pc(RelicSet):
    def __init__(self,
                graphic:str='',
                shortname:str = 'Firesmith 4pc',
                uptime:float = 1.0/3.0,
                **config):
        self.graphic = graphic
        self.shortname = shortname
        self.uptime = uptime

    def equipTo(self, char:BaseCharacter):
        char.DmgType['skill'] += 0.12
        char.fireDmg += 0.05 * self.uptime