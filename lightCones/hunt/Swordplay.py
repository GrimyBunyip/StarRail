from baseClasses.BaseCharacter import BaseCharacter
from baseClasses.BaseLightCone import BaseLightCone
from baseClasses.BuffEffect import BuffEffect

class Swordplay(BaseLightCone):
    def __init__(self, 
                stacks:int = 5,
                **config):
        self.loadConeStats('Swordplay')
        self.setSuperposition(config)
        self.stacks = stacks

    def equipTo(self, char:BaseCharacter):
        self.addStats(char)
        if char.path == self.path:
            char.stats['DMG'].append(BuffEffect(description=self.name,
                                    amount=0.06 + 0.02 * self.superposition,
                                    stacks=self.stacks))
        
if __name__ == '__main__':
    from settings.BaseConfiguration import Configuration
    Swordplay(**Configuration).print()