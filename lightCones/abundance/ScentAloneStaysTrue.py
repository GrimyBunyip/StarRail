from baseClasses.BaseCharacter import BaseCharacter
from baseClasses.BaseLightCone import BaseLightCone

class ScentAloneStaysTrue(BaseLightCone):
    def __init__(self,
                superposition:int=None,
                **config):
        self.loadConeStats('Scent Alone Stays True', shortname='Scent')
        self.setSuperposition(superposition,config)

    def equipTo(self, char:BaseCharacter):
        self.addStats(char)
        char.addStat('BreakEffect',description=self.name,amount=0.5+0.1*self.superposition)
                
if __name__ == '__main__':
    from settings.BaseConfiguration import Configuration
    ScentAloneStaysTrue(**Configuration).print()