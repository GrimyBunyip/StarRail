from baseClasses.BaseCharacter import BaseCharacter
from baseClasses.BaseLightCone import BaseLightCone

class ReturnToDarkness(BaseLightCone):
    def __init__(self, 
                **config):
        self.loadConeStats('Return to Darkness')
        self.setSuperposition(config)

    def equipTo(self, char:BaseCharacter):
        self.addBaseStats(char)
        if char.path == self.path:
            char.CR += 0.09 + 0.03 * self.superposition
        
if __name__ == '__main__':
    from settings.BaseConfiguration import Configuration
    ReturnToDarkness(**Configuration).print()