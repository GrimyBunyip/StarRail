from baseClasses.BaseCharacter import BaseCharacter
from baseClasses.BaseLightCone import BaseLightCone
from baseClasses.BuffEffect import BuffEffect

class EyesOfThePrey(BaseLightCone):
    def __init__(self,
                **config):
        self.loadConeStats('Eyes of the Prey')
        self.setSuperposition(config)

    def equipTo(self, char:BaseCharacter):
        self.addStats(char)
        if char.path == self.path:
            char.stats['EHR'].append(BuffEffect(description=self.name,
                                    amount=0.15 + 0.05 * self.superposition))
            char.stats['DMG'].append(BuffEffect(description=self.name,
                                    amount=0.18 + 0.06 * self.superposition,
                                    type='dot'))

if __name__ == '__main__':
    from settings.BaseConfiguration import Configuration
    EyesOfThePrey(**Configuration).print()