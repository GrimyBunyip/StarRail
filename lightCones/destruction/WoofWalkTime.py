from baseClasses.BaseCharacter import BaseCharacter
from baseClasses.BaseLightCone import BaseLightCone

class WoofWalkTime(BaseLightCone):
    def __init__(self,
                uptime:float = 1.0,
                superposition:int=None,
                **config):
        self.loadConeStats('Woof! Walk Time!')
        self.setSuperposition(superposition,config)
        self.uptime = uptime
        self.nameAffix = f'{uptime:.2f} Uptime'

    def equipTo(self, char:BaseCharacter):
        self.addStats(char)
        if char.path == self.path:
            char.addStat('ATK.percent',description=self.name,
                                    amount=0.075 + 0.025 * self.superposition)
            char.addStat('DMG',description=self.name,
                                    amount=0.12 + 0.04 * self.superpositio,
                                    uptime=self.uptime)
        
if __name__ == '__main__':
    from settings.BaseConfiguration import Configuration
    WoofWalkTime(**Configuration).print()