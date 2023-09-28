from baseClasses.BaseCharacter import BaseCharacter
from baseClasses.BaseLightCone import BaseLightCone
from baseClasses.BuffEffect import BuffEffect

class TextureOfMemories(BaseLightCone):
    def __init__(self,
                uptime:float=1.0,
                **config):
        self.loadConeStats('TextureOfMemories')
        self.setSuperposition(config)
        self.uptime = uptime

    def equipTo(self, char:BaseCharacter):
        self.addStats(char)
        if char.path == self.path:
            char.stats['RES'].append(BuffEffect(description=self.name,
                                    amount=0.06 + 0.02 * self.superposition))
            char.stats['DmgReduction'].append(BuffEffect(description=self.name,
                                        amount=0.09 + 0.03 * self.superposition,
                                        mathType='reductionMult',
                                        uptime=self.uptime))
            
if __name__ == '__main__':
    from settings.BaseConfiguration import Configuration
    TextureOfMemories(**Configuration).print()