from baseClasses.BaseCharacter import BaseCharacter
from baseClasses.BaseLightCone import BaseLightCone

class NightOfFright(BaseLightCone):
    def __init__(self,
                superposition:int=None,
                **config):
        self.loadConeStats('Night of Fright')
        self.setSuperposition(superposition,config)

    def equipTo(self, char:BaseCharacter):
        self.addStats(char)
        if char.path == self.path:
            char.addStat('ER', description=self.name,
                        amount=0.10 + 0.02 * self.superposition)
        
if __name__ == '__main__':
    from settings.BaseConfiguration import Configuration
    NightOfFright(**Configuration).print()