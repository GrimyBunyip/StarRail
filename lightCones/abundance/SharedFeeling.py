from baseClasses.BaseCharacter import BaseCharacter
from baseClasses.BaseLightCone import BaseLightCone

class SharedFeeling(BaseLightCone):
    def __init__(self,
                superposition:int=None,
                **config):
        self.loadConeStats('Shared Feeling', shortname='Shared')
        self.setSuperposition(superposition,config)

    def equipTo(self, char:BaseCharacter):
        self.addStats(char)
        char.addStat('Heal', description=self.name,
                    amount=0.075 + 0.025 * self.superposition,)
                
if __name__ == '__main__':
    from settings.BaseConfiguration import Configuration
    SharedFeeling(**Configuration).print()