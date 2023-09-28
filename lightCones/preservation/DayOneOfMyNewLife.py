from baseClasses.BaseCharacter import BaseCharacter
from baseClasses.BaseLightCone import BaseLightCone
from baseClasses.BuffEffect import BuffEffect

class DayOneOfMyNewLife(BaseLightCone):
    def __init__(self,
                **config):
        self.loadConeStats('Day One of My New Life')
        self.setSuperposition(config)

    def equipTo(self, char:BaseCharacter):
        self.addStats(char)
        if char.path == self.path:
            char.stats['DEF'].append(BuffEffect(description=self.name,
                                    amount=0.14 + 0.02 * self.superposition,
                                    mathType='percent'))
            char.stats['AllRes'].append(BuffEffect(description=self.name,
                                    amount=0.07 + 0.01 * self.superposition))
            
if __name__ == '__main__':
    from settings.BaseConfiguration import Configuration
    DayOneOfMyNewLife(**Configuration).print()