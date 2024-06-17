from baseClasses.BaseCharacter import BaseCharacter
from baseClasses.BaseLightCone import BaseLightCone

class PoisedToBloom(BaseLightCone):
    def __init__(self,
                **config):
        self.loadConeStats('Poised to Bloom')
        self.setSuperposition(config)

    def equipTo(self, char:BaseCharacter):
        self.addStats(char)
        if char.path == self.path:
            char.addStat('ATK.percent',description=self.name,amount=0.12 + 0.04 * self.superposition)
            
if __name__ == '__main__':
    from settings.BaseConfiguration import Configuration
    PoisedToBloom(**Configuration).print()