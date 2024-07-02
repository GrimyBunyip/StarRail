from baseClasses.BaseCharacter import BaseCharacter
from baseClasses.BaseLightCone import BaseLightCone

class Swordplay(BaseLightCone):
    def __init__(self, 
                stacks:int = 5,
                superposition:int=None,
                **config):
        self.loadConeStats('Swordplay')
        self.setSuperposition(superposition,config)
        self.stacks = stacks

    def equipTo(self, char:BaseCharacter):
        self.addStats(char)
        if char.path == self.path:
            char.addStat('DMG',description=self.name,
                                    amount=0.06 + 0.02 * self.superposition,
                                    stacks=self.stacks)
        
if __name__ == '__main__':
    from settings.BaseConfiguration import Configuration
    Swordplay(**Configuration).print()