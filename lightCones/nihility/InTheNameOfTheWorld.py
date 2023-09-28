from baseClasses.BaseCharacter import BaseCharacter
from baseClasses.BaseLightCone import BaseLightCone
from baseClasses.BuffEffect import BuffEffect

class InTheNameOfTheWorld(BaseLightCone):
    def __init__(self,
                uptime:float = 1.0,
                **config):
        self.loadConeStats('In the Name of the World')
        self.setSuperposition(config)
        self.uptime=uptime

    def equipTo(self, char:BaseCharacter):
        self.addStats(char)
        if char.path == self.path:
            char.stats['DMG'].append(BuffEffect(description=self.name,
                                    amount=0.20 + 0.04 * self.superposition,
                                    uptime=self.uptime))
            char.stats['ATK'].append(BuffEffect(description=self.name,
                                    amount=0.20 + 0.04 * self.superposition,
                                    mathType='percent'))
            char.stats['EHR'].append(BuffEffect(description=self.name,
                                    amount=0.15 + 0.03 * self.superposition,
                                    type='skill'))
            
if __name__ == '__main__':
    from settings.BaseConfiguration import Configuration
    InTheNameOfTheWorld(**Configuration).print()