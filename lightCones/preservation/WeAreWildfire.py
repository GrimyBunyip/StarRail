from baseClasses.BaseCharacter import BaseCharacter
from baseClasses.BaseLightCone import BaseLightCone

class WeAreWildfire(BaseLightCone):
    def __init__(self,
                uptime:float=1.0,
                **config):
        self.loadConeStats('We Are Wildfire')
        self.setSuperposition(config)
        self.uptime = uptime

    def equipTo(self, char:BaseCharacter):
        self.addBaseStats(char)
        if char.path == self.path:
            char.dmgReduction += ( 0.06 + 0.02 * self.superposition ) * self.uptime
            # not implemented: immediate heal
            
if __name__ == '__main__':
    from settings.BaseConfiguration import Configuration
    WeAreWildfire(**Configuration).print()