from baseClasses.BaseCharacter import BaseCharacter
from baseClasses.BaseLightCone import BaseLightCone

class WorrisomeBlissful(BaseLightCone):
    def __init__(self,
                stacks:float = 2.0,
                superposition:int=None,
                **config):
        self.loadConeStats('Worrisome, Blissful')
        self.setSuperposition(superposition,config)
        self.stacks = stacks

    def equipTo(self, char:BaseCharacter):
        self.addStats(char)
        if char.path == self.path:
            char.addStat('CR',description=self.name,
                                    amount=0.15 + 0.03 * self.superposition)
            char.addStat('CD',description=self.name,
                                    amount=0.10 + 0.02 * self.superposition,
                                    stacks=self.stacks)
            char.addStat('DMG',description=self.name,
                                    amount=0.25 + 0.05 * self.superposition,
                                    type=['followup'])
        
if __name__ == '__main__':
    from settings.BaseConfiguration import Configuration
    WorrisomeBlissful(**Configuration).print()