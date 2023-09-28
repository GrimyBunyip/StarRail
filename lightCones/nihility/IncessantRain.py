from baseClasses.BaseCharacter import BaseCharacter
from baseClasses.BaseLightCone import BaseLightCone
from baseClasses.BuffEffect import BuffEffect

class IncessantRain(BaseLightCone):
    def __init__(self,
                uptime:float=1.0,
                uptimeAether:float=1.0,
                **config):
        self.loadConeStats('Incessant Rain')
        self.setSuperposition(config)
        self.uptime = uptime
        self.uptimeAether = uptimeAether

    def equipTo(self, char:BaseCharacter):
        self.addStats(char)
        if char.path == self.path:
            char.addStat('EHR',description=self.name,
                                    amount=0.20 + 0.04 * self.superposition)
            char.addStat('CR',description=self.name,
                                    amount=0.10 + 0.02 * self.superposition,
                                    uptime=self.uptime)
            char.addStat('DMG',description=self.name,
                                    amount=0.10 + 0.02 * self.superposition,
                                    uptime=self.uptimeAether)
            char.addStat('Vulnerability',description=self.name,
                                                amount=0.1 + 0.02 * self.superposition)
            
if __name__ == '__main__':
    from settings.BaseConfiguration import Configuration
    IncessantRain(**Configuration).print()