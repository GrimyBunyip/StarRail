from baseClasses.BaseCharacter import BaseCharacter
from baseClasses.BaseLightCone import BaseLightCone

class IVentureForthToHunt(BaseLightCone):
    def __init__(self,
                superposition:int=None,
                stacks:int=6,
                **config):
        self.loadConeStats('I Venture Forth to Hunt')
        self.setSuperposition(superposition,config)
        self.stacks = stacks

    def equipTo(self, char:BaseCharacter):
        char.addStat('CR', description=self.name, amount=0.125 + 0.025 * self.superposition)
        char.addStat('DefShred',description=self.name,
                                amount=0.08 + 0.01 * self.superposition,
                                stacks=self.stacks,
                                type=['ultimate'])
        
if __name__ == '__main__':
    from settings.BaseConfiguration import Configuration
    IVentureForthToHunt(**Configuration).print()