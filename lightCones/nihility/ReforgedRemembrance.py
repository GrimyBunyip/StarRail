from baseClasses.BaseCharacter import BaseCharacter
from baseClasses.BaseLightCone import BaseLightCone

class ReforgedRemembrance(BaseLightCone):
    def __init__(self,
                stacks:float=4.0,
                **config):
        self.loadConeStats('Reforged Remembrance')
        self.setSuperposition(config)
        self.stacks = stacks

    def equipTo(self, char:BaseCharacter):
        self.addStats(char)
        if char.path == self.path:
            char.addStat('EHR',description=self.name,
                                    amount=0.35 + 0.05 * self.superposition)
            char.addStat('ATK.percent',description=self.name,
                                    amount=0.04 + 0.01 * self.superposition, stacks=self.stacks)
            char.addStat('DefShred',description=self.name,
                                    amount=0.065 + 0.007 * self.superposition, stacks=self.stacks)
            
if __name__ == '__main__':
    from settings.BaseConfiguration import Configuration
    ReforgedRemembrance(**Configuration).print()