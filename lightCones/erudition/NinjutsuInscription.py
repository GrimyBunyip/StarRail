from baseClasses.BaseCharacter import BaseCharacter
from baseClasses.BaseLightCone import BaseLightCone

class NinjutsuInscription(BaseLightCone):
    def __init__(self,
                superposition:int=None,
                **config):
        self.loadConeStats('Ninjutsu Inscription: Dazzling Evilbreaker', shortname='Ninjutsu')
        self.setSuperposition(superposition,config)

    def equipTo(self, char:BaseCharacter):
        self.addStats(char)
        if char.path == self.path:
            char.addStat('BreakEffect',description=self.name,
                                    amount=0.50 + 0.10 * self.superposition)
        
if __name__ == '__main__':
    from settings.BaseConfiguration import Configuration
    NinjutsuInscription(**Configuration).print()