from baseClasses.BaseCharacter import BaseCharacter
from baseClasses.BaseLightCone import BaseLightCone
from baseClasses.BuffEffect import BuffEffect

class LandausChoice(BaseLightCone):
    def __init__(self,
                **config):
        self.loadConeStats('Landau\'s Choice')
        self.setSuperposition(config)

    def equipTo(self, char:BaseCharacter):
        self.addStats(char)
        if char.path == self.path:
            char.stats['Taunt'].append(BuffEffect(description=self.name,
                                        amount=2.0,
                                        mathType='percent'))
            char.stats['DmgReduction'].append(BuffEffect(description=self.name,
                                        amount=0.14 + 0.02 * self.superposition,
                                        mathType='reductionMult'))
            
if __name__ == '__main__':
    from settings.BaseConfiguration import Configuration
    LandausChoice(**Configuration).print()