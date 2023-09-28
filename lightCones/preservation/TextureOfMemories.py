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
            char.Res += 0.06 + 0.02 * self.superposition
            char.dmgReduction += ( 0.09 + 0.03 * self.superposition ) * self.uptime
            
if __name__ == '__main__':
    from settings.BaseConfiguration import Configuration
    TextureOfMemories(**Configuration).print()