from baseClasses.BaseCharacter import BaseCharacter
from baseClasses.BaseLightCone import BaseLightCone
from baseClasses.BuffEffect import BuffEffect

class BeforeDawn(BaseLightCone):
    def __init__(self,
                uptime:float=1.0,
                **config):
        self.loadConeStats('Before Dawn')
        self.setSuperposition(config)
        self.uptime = uptime

    def equipTo(self, char:BaseCharacter):
        self.addStats(char)
        if char.path == self.path:
            char.CD += 0.30 + 0.06 * self.superposition
            char.DmgType['skill'] += 0.15 + 0.03 * self.superposition
            char.DmgType['ultimate'] += 0.15 + 0.03 * self.superposition
            char.DmgType['followup'] += ( 0.40 + 0.08 * self. superposition ) * self.uptime
            
if __name__ == '__main__':
    from settings.BaseConfiguration import Configuration
    BeforeDawn(**Configuration).print()