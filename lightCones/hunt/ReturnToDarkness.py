from baseClasses.BaseCharacter import BaseCharacter
from baseClasses.BaseLightCone import BaseLightCone

class ReturnToDarkness(BaseLightCone):
    def __init__(self, 
                superposition:int=None,
                **config):
        self.loadConeStats('Return to Darkness')
        self.setSuperposition(superposition,config)

    def equipTo(self, char:BaseCharacter):
        self.addStats(char)
        if char.path == self.path:
            char.addStat('CR',description=self.name,
                                    amount=0.09 + 0.03 * self.superposition)
        
if __name__ == '__main__':
    from settings.BaseConfiguration import Configuration
    ReturnToDarkness(**Configuration).print()