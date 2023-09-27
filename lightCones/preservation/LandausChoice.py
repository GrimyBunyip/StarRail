from baseClasses.BaseCharacter import BaseCharacter
from baseClasses.BaseLightCone import BaseLightCone

class LandausChoice(BaseLightCone):
    def __init__(self,
                **config):
        self.loadConeStats('Landau\'s Choice')
        self.setSuperposition(config)

    def equipTo(self, char:BaseCharacter):
        self.addBaseStats(char)
        if char.path == self.path:
            char.percTaunt += 2.0
            char.dmgReduction += 0.14 + 0.02 * self.superposition
            
if __name__ == '__main__':
    from settings.BaseConfiguration import Configuration
    LandausChoice(**Configuration).print()