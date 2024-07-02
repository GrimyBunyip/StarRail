from baseClasses.BaseCharacter import BaseCharacter
from baseClasses.BaseLightCone import BaseLightCone

class OnlySilenceRemains(BaseLightCone):
    def __init__(self, 
                superposition:int=None,
                **config):
        self.loadConeStats('Only Silence Remains')
        self.setSuperposition(superposition,config)

    def equipTo(self, char:BaseCharacter):
        self.addStats(char)
        if char.path == self.path:
            char.addStat('CR',description=self.name,
                                    amount=( 0.09 + 0.03 * self.superposition ) if char.numEnemies <= 2 else 0.0)
            char.addStat('ATK.percent',description=self.name,
                                    amount=0.12 + 0.04 * self.superposition)
        
if __name__ == '__main__':
    from settings.BaseConfiguration import Configuration
    OnlySilenceRemains(**Configuration).print()