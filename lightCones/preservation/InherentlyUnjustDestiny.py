from baseClasses.BaseCharacter import BaseCharacter
from baseClasses.BaseLightCone import BaseLightCone
from baseClasses.BaseMV import BaseMV

class InherentlyUnjustDestiny(BaseLightCone):
    def __init__(self,
                 uptime:float=1.0,
                superposition:int=None,
                **config):
        self.loadConeStats('Inherently Unjust Destiny')
        self.setSuperposition(superposition,config)
        self.uptime = uptime

    def equipTo(self, char:BaseCharacter):
        self.addStats(char)
        if char.path == self.path:
            char.addStat('DEF.percent',description=self.name,
                                    amount=0.30 + 0.06 * self.superposition)
            char.addStat('CD',description=self.name,
                         amount = 0.34 + 0.06 * self.superposition,
                         uptime=self.uptime)
            
if __name__ == '__main__':
    from settings.BaseConfiguration import Configuration
    InherentlyUnjustDestiny(**Configuration).print()