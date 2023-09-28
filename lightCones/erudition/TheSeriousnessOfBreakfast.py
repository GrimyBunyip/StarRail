from baseClasses.BaseCharacter import BaseCharacter
from baseClasses.BaseLightCone import BaseLightCone
from baseClasses.BuffEffect import BuffEffect

class TheSeriousnessOfBreakfast(BaseLightCone):
    def __init__(self,
                stacks:float=3.0,
                **config):
        self.loadConeStats('The Seriousness of Breakfast')
        self.setSuperposition(config)
        self.stacks = stacks

    def equipTo(self, char:BaseCharacter):
        self.addStats(char)
        if char.path == self.path:
            char.Dmg += 0.09 + 0.03 * self.superposition
            char.percAtk += ( 0.03 + 0.01 * self.superposition ) * self.stacks
        
if __name__ == '__main__':
    from settings.BaseConfiguration import Configuration
    TheSeriousnessOfBreakfast(**Configuration).print()