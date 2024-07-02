from baseClasses.BaseCharacter import BaseCharacter
from baseClasses.BaseLightCone import BaseLightCone

class DanceAtSunset(BaseLightCone):
    def __init__(self,
                uptime:float = 1.0,
                stacks:float = 2.0,
                superposition:int=None,
                **config):
        self.loadConeStats('Dance at Sunset')
        self.setSuperposition(superposition,config)
        self.uptime = uptime
        self.stacks = stacks

    def equipTo(self, char:BaseCharacter):
        self.addStats(char)
        if char.path == self.path:
            char.addStat('CD',description=self.name,
                                    amount=0.30 + 0.06 * self.superposition)
            char.addStat('DMG',description=self.name,
                                    amount=0.30 + 0.06 * self.superposition,
                                    uptime=self.uptime,
                                    stacks=self.stacks,
                                    type=['followup'])
        
if __name__ == '__main__':
    from settings.BaseConfiguration import Configuration
    DanceAtSunset(**Configuration).print()