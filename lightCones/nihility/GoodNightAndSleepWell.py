from baseClasses.BaseCharacter import BaseCharacter
from baseClasses.BaseLightCone import BaseLightCone
from baseClasses.BuffEffect import BuffEffect

class GoodNightAndSleepWell(BaseLightCone):
    def __init__(self,
                stacks:float=3.0,
                **config):
        self.loadConeStats('Good Night and Sleep Well')
        self.setSuperposition(config)
        self.stacks = stacks

    def equipTo(self, char:BaseCharacter):
        self.addStats(char)
        if char.path == self.path:
            char.stats['DMG'].append(BuffEffect(description=self.name,
                                    amount=0.09 + 0.03 * self.superposition,
                                    stacks=self.stacks))

if __name__ == '__main__':
    from settings.BaseConfiguration import Configuration
    GoodNightAndSleepWell(**Configuration).print()