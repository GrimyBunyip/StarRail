from baseClasses.BaseCharacter import BaseCharacter
from baseClasses.BaseLightCone import BaseLightCone

class DestinysThreadsForewoven(BaseLightCone):
    def __init__(self,
                 defense:float=4000,
                superposition:int=None,
                **config):
        self.loadConeStats('Destiny\'s Threads Forewoven', shortname='Destiny')
        self.setSuperposition(superposition,config)
        self.defense = min(4000,defense)

    def equipTo(self, char:BaseCharacter):
        self.addStats(char)
        if char.path == self.path:
            char.addStat('RES',description=self.name,
                                amount=0.10 + 0.02 * self.superposition)
            char.addStat('DMG',description=self.name,
                                amount=self.defense * ( 0.007 + 0.001 * self.superposition ) / 100.0 )
            
if __name__ == '__main__':
    from settings.BaseConfiguration import Configuration
    DestinysThreadsForewoven(**Configuration).print()