from baseClasses.BaseCharacter import BaseCharacter
from baseClasses.BaseLightCone import BaseLightCone

class PastAndFuture(BaseLightCone):
    def __init__(self,
                superposition:int=None,
                **config):
        self.loadConeStats('Past and Future')
        self.setSuperposition(superposition,config)

    def equipTo(self, char:BaseCharacter):
        self.addStats(char)
        if char.path == self.path:
            pass #harmony cones not yet implemented fully
            
if __name__ == '__main__':
    from settings.BaseConfiguration import Configuration
    PastAndFuture(**Configuration).print()