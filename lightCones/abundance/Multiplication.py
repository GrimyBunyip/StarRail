from baseClasses.BaseCharacter import BaseCharacter
from baseClasses.BaseLightCone import BaseLightCone

class Multiplication(BaseLightCone):
    def __init__(self,
                superposition:int=None,
                **config):
        self.loadConeStats('Multiplication')
        self.setSuperposition(superposition,config)

    def equipTo(self, char:BaseCharacter):
        self.addStats(char)
        if char.path == self.path:
            char.addStat('AdvanceForward', description=self.name,
                        amount=0.10 + 0.02 * self.superposition,
                        type=['basic'])
        
if __name__ == '__main__':
    from settings.BaseConfiguration import Configuration
    Multiplication(**Configuration).print()