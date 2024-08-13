from baseClasses.BaseCharacter import BaseCharacter
from baseClasses.BaseLightCone import BaseLightCone

class EchoesOfTheCoffin(BaseLightCone):
    def __init__(self,
                superposition:int=None,
                **config):
        self.loadConeStats('Echoes of the Coffin', shortname='Coffin')
        self.setSuperposition(superposition,config)

    def equipTo(self, char:BaseCharacter):
        self.addStats(char)
        if char.path == self.path:
            char.addStat('ATK.percent', description=self.name,
                        amount=0.20 + 0.04 * self.superposition)
        
if __name__ == '__main__':
    from settings.BaseConfiguration import Configuration
    EchoesOfTheCoffin(**Configuration).print()