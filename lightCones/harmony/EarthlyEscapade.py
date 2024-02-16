from baseClasses.BaseCharacter import BaseCharacter
from baseClasses.BaseLightCone import BaseLightCone

class EarthlyEscapade(BaseLightCone):
    def __init__(self,
                **config):
        self.loadConeStats('Earthly Escapade')
        self.setSuperposition(config)

    def equipTo(self, char:BaseCharacter):
        self.addStats(char)
        if char.path == self.path:
            char.addStat('CD',description=self.name,amount=0.25 + 0.07 * self.superposition)
            
if __name__ == '__main__':
    from settings.BaseConfiguration import Configuration
    EarthlyEscapade(**Configuration).print()