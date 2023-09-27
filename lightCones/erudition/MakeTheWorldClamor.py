from baseClasses.BaseCharacter import BaseCharacter
from baseClasses.BaseLightCone import BaseLightCone

class MakeTheWorldClamor(BaseLightCone):
    def __init__(self,
                **config):
        self.loadConeStats('Make the World Clamor')
        self.setSuperposition(config)

    def equipTo(self, char:BaseCharacter):
        self.addBaseStats(char)
        if char.path == self.path:
            char.percAtk += 0.24 + 0.08 * self.superposition
            char.initialEnergy += 17.0 + 3.0 * self.superposition
            
if __name__ == '__main__':
    from settings.BaseConfiguration import Configuration
    MakeTheWorldClamor(**Configuration).print()