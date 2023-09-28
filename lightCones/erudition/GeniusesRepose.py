from baseClasses.BaseCharacter import BaseCharacter
from baseClasses.BaseLightCone import BaseLightCone
from baseClasses.BuffEffect import BuffEffect

class GeniusesRepose(BaseLightCone):
    def __init__(self,
                uptime:float=1.0,
                **config):
        self.loadConeStats('Geniuses\' Repose')
        self.setSuperposition(config)
        self.uptime = uptime

    def equipTo(self, char:BaseCharacter):
        self.addStats(char)
        if char.path == self.path:
            char.stats['ATK'].append(BuffEffect(description=self.name,
                                    amount=0.12 + 0.04 * self.superposition,
                                    mathType='percent'))
            char.stats['CD'].append(BuffEffect(description=self.name,
                                    amount=0.18 + 0.06 * self. superposition,
                                    uptime=self.uptime))
            
if __name__ == '__main__':
    from settings.BaseConfiguration import Configuration
    GeniusesRepose(**Configuration).print()