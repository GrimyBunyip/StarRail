from baseClasses.BaseCharacter import BaseCharacter
from baseClasses.BaseLightCone import BaseLightCone

class SomethingIrreplaceable(BaseLightCone):
    def __init__(self,
                uptime:float = 1.0,
                **config):
        self.loadConeStats('Something Irreplaceable')
        self.setSuperposition(config)
        self.uptime = uptime

    def equipTo(self, char:BaseCharacter):
        self.addStats(char)
        if char.path == self.path:
            char.addStat('ATK.percent',description=self.name,
                                    amount=0.20 + 0.04 * self.superposition)
            char.addStat('DMG',description=self.name,
                                    amount=0.20 + 0.04 * self.superposition,
                                    uptime=self.uptime)
        
if __name__ == '__main__':
    from settings.BaseConfiguration import Configuration
    SomethingIrreplaceable(**Configuration).print()