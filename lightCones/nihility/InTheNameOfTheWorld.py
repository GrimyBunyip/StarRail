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
            char.Dmg += ( 0.20 + 0.04 * self.superposition ) * self.uptime
            char.percAtkType['skill'] += 0.20 + 0.04 * self.superposition
            # also boosts skill EHR, but not implementing that atm
            
if __name__ == '__main__':
    from settings.BaseConfiguration import Configuration
    InTheNameOfTheWorld(**Configuration).print()