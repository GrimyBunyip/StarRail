from baseClasses.BaseCharacter import BaseCharacter
from baseClasses.BaseLightCone import BaseLightCone
from baseClasses.BuffEffect import BuffEffect

class RiverFlowsInSpring(BaseLightCone):
    def __init__(self, 
                uptime:float = 1.0,
                **config):
        self.loadConeStats('River Flows in Spring')
        self.setSuperposition(config)
        self.uptime = uptime

    def equipTo(self, char:BaseCharacter):
        self.addStats(char)
        if char.path == self.path:
            char.addStat('SPD.percent',description=self.name,
                                    amount=0.07 + 0.01 * self.superposition,
                                    uptime=self.uptime)
            char.addStat('DMG',description=self.name,
                                    amount=0.09 + 0.03 * self.superposition,
                                    uptime=self.uptime)
        
if __name__ == '__main__':
    from settings.BaseConfiguration import Configuration
    RiverFlowsInSpring(**Configuration).print()