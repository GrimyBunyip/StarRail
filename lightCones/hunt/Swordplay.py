from baseClasses.BaseCharacter import BaseCharacter
from baseClasses.BaseLightCone import BaseLightCone

class Swordplay(BaseLightCone):
    def __init__(self, 
                stacks:int = 5,
                **config):
        self.loadConeStats('Swordplay')
        self.setSuperposition(config)
        self.stacks = stacks

    def equipTo(self, char:BaseCharacter):
        self.addBaseStats(char)
        if char.path == self.path:
            char.Dmg += ( 0.06 + 0.02 * self.superposition ) * self.stacks
        
if __name__ == '__main__':
    from settings.BaseConfiguration import Configuration
    Swordplay(**Configuration).print()