from baseClasses.BaseCharacter import BaseCharacter
from baseClasses.BaseLightCone import BaseLightCone

class MemoriesOfThePast(BaseLightCone):
    def __init__(self,
                **config):
        self.loadConeStats('Memories of the Past')
        self.setSuperposition(config)

    def equipTo(self, char:BaseCharacter):
        self.addStats(char)
        if char.path == self.path:
            char.addStat('BreakEffect',description=self.name,amount=0.21 + 0.07 * self.superposition)
            char.addStat('BonusEnergyAttack',description=self.name,
                                                    amount=3.0 + 1.0 * self.superposition)
            
if __name__ == '__main__':
    from settings.BaseConfiguration import Configuration
    MemoriesOfThePast(**Configuration).print()