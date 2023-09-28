from baseClasses.BaseCharacter import BaseCharacter
from baseClasses.BaseLightCone import BaseLightCone
from baseClasses.BuffEffect import BuffEffect

class MemoriesOfThePast(BaseLightCone):
    def __init__(self,
                **config):
        self.loadConeStats('Memories of the Past')
        self.setSuperposition(config)

    def equipTo(self, char:BaseCharacter):
        self.addStats(char)
        if char.path == self.path:
            char.stats['BonusEnergyAttack'].append(BuffEffect(description=self.name,
                                                    amount=3.0 + 1.0 * self.superposition))
            
if __name__ == '__main__':
    from settings.BaseConfiguration import Configuration
    MemoriesOfThePast(**Configuration).print()