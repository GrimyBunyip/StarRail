from baseClasses.BaseCharacter import BaseCharacter
from baseClasses.BaseLightCone import BaseLightCone

class AlongThePassingShore(BaseLightCone):
    def __init__(self,
                **config):
        self.loadConeStats('Along the Passing Shore')
        self.setSuperposition(config)

    def equipTo(self, char:BaseCharacter):
        self.addStats(char)
        if char.path == self.path:
            char.addStat('CD',description=self.name,
                                    amount=0.30 + 0.06 * self.superposition)
            char.addStat('DMG',description=self.name,
                                    amount=0.20 + 0.04 * self.superposition)
            char.addStat('DMG',description=self.name,
                                    amount=0.20 + 0.04 * self.superposition,
                                    type=['ultimate'])
            
if __name__ == '__main__':
    from settings.BaseConfiguration import Configuration
    AlongThePassingShore(**Configuration).print()