from baseClasses.BaseCharacter import BaseCharacter
from baseClasses.BaseLightCone import BaseLightCone
from baseClasses.BuffEffect import BuffEffect
from baseClasses.BaseMV import BaseMV

class PatienceIsAllYouNeed(BaseLightCone):
    def __init__(self,
                stacks:float=3.0,
                **config):
        self.loadConeStats('Patience Is All You Need')
        self.setSuperposition(config)
        self.stacks = stacks

    def equipTo(self, char:BaseCharacter):
        self.addStats(char)
        if char.path == self.path:
            char.addStat('DMG',description=self.name,
                                    amount=0.20 + 0.04 * self.superposition)
            char.addStat('SPD',description=self.name,
                                    amount=0.04 + 0.008 * self.superposition,
                                    stacks=self.stacks)
            
            char.motionValueDict['dot'] = [BaseMV(type='dot',area='all', stat='atk', value=0.5+0.1*self.superposition)] + char.motionValueDict['dot'] if 'dot' in char.motionValueDict else []
            
if __name__ == '__main__':
    from settings.BaseConfiguration import Configuration
    PatienceIsAllYouNeed(**Configuration).print()