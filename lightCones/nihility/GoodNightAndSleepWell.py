from baseClasses.BaseCharacter import BaseCharacter
from baseClasses.BaseLightCone import BaseLightCone

class GoodNightAndSleepWell(BaseLightCone):
    def __init__(self,
                stacks:float=3.0,
                **config):
        self.loadConeStats(name='Good Night and Sleep Well', shortname='Good Night')
        self.setSuperposition(config)
        self.stacks = stacks

    def equipTo(self, char:BaseCharacter):
        self.addStats(char)
        if char.path == self.path:
            char.addStat('DMG',description=self.name,
                                    amount=0.09 + 0.03 * self.superposition,
                                    stacks=self.stacks)

if __name__ == '__main__':
    from settings.BaseConfiguration import Configuration
    GoodNightAndSleepWell(**Configuration).print()