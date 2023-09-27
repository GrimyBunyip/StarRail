from baseClasses.BaseCharacter import BaseCharacter
from baseClasses.BaseLightCone import BaseLightCone

class UnderTheBlueSky(BaseLightCone):
    def __init__(self,
                uptime:float = 1.0,
                **config):
        self.loadConeStats('Under the Blue Sky')
        self.setSuperposition(config)
        self.uptime = uptime

    def equipTo(self, char:BaseCharacter):
        self.addBaseStats(char)
        if char.path == self.path:
            char.percAtk += 0.12 + 0.04 * self.superposition
            char.CR += ( 0.09 + 0.03 * self.superposition ) * self.uptime
        
if __name__ == '__main__':
    from settings.BaseConfiguration import Configuration
    UnderTheBlueSky(**Configuration).print()