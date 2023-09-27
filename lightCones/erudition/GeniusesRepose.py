from baseClasses.BaseCharacter import BaseCharacter
from baseClasses.BaseLightCone import BaseLightCone

class GeniusesRepose(BaseLightCone):
    def __init__(self,
                uptime:float=1.0,
                **config):
        self.loadConeStats('Geniuses\' Repose')
        self.setSuperposition(config)
        self.uptime = uptime

    def equipTo(self, char:BaseCharacter):
        self.addBaseStats(char)
        if char.path == self.path:
            char.percAtk += 0.12 + 0.04 * self.superposition
            char.CD += ( 0.18 + 0.06 * self. superposition ) * self.uptime
            
if __name__ == '__main__':
    from settings.BaseConfiguration import Configuration
    GeniusesRepose(**Configuration).print()