from baseClasses.BaseCharacter import BaseCharacter
from baseClasses.RelicSet import RelicSet
from baseClasses.BuffEffect import BuffEffect

class ThiefOfShootingMeteor2pc(RelicSet):
    def __init__(self,
                graphic:str='',
                shortname:str = 'Thief 2pc',
                **config):
        self.graphic = graphic
        self.shortname = shortname

    def equipTo(self, char:BaseCharacter):
        char.stats['BreakEffect'].append(BuffEffect(description=self.shortname,
                                        amount=0.16))
        
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
        char.stats['BreakEffect'].append(BuffEffect(description=self.shortname,
                                        amount=0.16))
        # energy mechanics not really implemented