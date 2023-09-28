from baseClasses.BaseCharacter import BaseCharacter
from baseClasses.BaseLightCone import BaseLightCone
from baseClasses.BuffEffect import BuffEffect
from baseClasses.BaseMV import BaseMV

class TrendOfTheUniversalMarket(BaseLightCone):
    def __init__(self,
                **config):
        self.loadConeStats('Trend of the Universal Market')
        self.setSuperposition(config)

    def equipTo(self, char:BaseCharacter):
        self.addStats(char)
        if char.path == self.path:
            char.percDef += 0.12 + 0.04 * self.superposition
            char.motionValueDict['dot'] = [BaseMV(type='dot',area='single', stat='def', value=0.3+0.1*self.superposition)] + char.motionValueDict['dot'] if 'dot' in char.motionValueDict else []
            
if __name__ == '__main__':
    from settings.BaseConfiguration import Configuration
    TrendOfTheUniversalMarket(**Configuration).print()