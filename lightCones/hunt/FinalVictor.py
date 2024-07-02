from baseClasses.BaseCharacter import BaseCharacter
from baseClasses.BaseLightCone import BaseLightCone

class FinalVictor(BaseLightCone):
    def __init__(self,
                stacks:float = 2.57,
                superposition:int=None,
                **config):
        self.loadConeStats('Final Victor')
        self.setSuperposition(superposition,config)
        self.stacks = stacks

    def equipTo(self, char:BaseCharacter):
        self.addStats(char)
        if char.path == self.path:
            char.addStat('ATK.percent',description=self.name,
                                    amount=0.10 + 0.02 * self.superposition)
            char.addStat('CD',description='Final Victor Cone',
                                    amount=0.07 + 0.01 * self.superposition,
                                    stacks=self.stacks)
        
if __name__ == '__main__':
    from settings.BaseConfiguration import Configuration
    FinalVictor(**Configuration).print()