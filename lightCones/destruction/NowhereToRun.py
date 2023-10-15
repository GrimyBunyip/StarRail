from baseClasses.BaseCharacter import BaseCharacter
from baseClasses.BaseLightCone import BaseLightCone

class NowhereToRun(BaseLightCone):
    def __init__(self,
                **config):
        self.loadConeStats('Nowhere to Run')
        self.setSuperposition(config)

    def equipTo(self, char:BaseCharacter):
        self.addStats(char)
        if char.path == self.path:
            char.addStat('ATK.percent',description=self.name,
                                    amount=0.24 + 0.06 * self.superposition)
        
if __name__ == '__main__':
    from settings.BaseConfiguration import Configuration
    NowhereToRun(**Configuration).print()