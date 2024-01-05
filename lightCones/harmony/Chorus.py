from baseClasses.BaseCharacter import BaseCharacter
from baseClasses.BaseLightCone import BaseLightCone

class Chorus(BaseLightCone):
    def __init__(self,
                **config):
        self.loadConeStats('Chorus')
        self.setSuperposition(config)

    def equipTo(self, char:BaseCharacter):
        self.addStats(char)
                    
if __name__ == '__main__':
    from settings.BaseConfiguration import Configuration
    Chorus(**Configuration).print()