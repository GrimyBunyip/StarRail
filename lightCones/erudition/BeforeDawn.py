from baseClasses.BaseCharacter import BaseCharacter
from baseClasses.BaseLightCone import BaseLightCone

class BeforeDawn(BaseLightCone):
    def __init__(self,
                uptime:float=1.0,
                **config):
        self.loadConeStats('Before Dawn')
        self.setSuperposition(config)
        self.uptime = uptime
        self.nameAffix = f'{uptime:.2f} Uptime'

    def equipTo(self, char:BaseCharacter):
        self.addStats(char)
        if char.path == self.path:
            char.addStat('CD',description=self.name,
                                    amount=0.30 + 0.06 * self.superposition)
            char.addStat('DMG',description=self.name,
                                    amount=0.15 + 0.03 * self.superposition,
                                    type=['skill','ultimate'])
            char.addStat('DMG',description=self.name,
                                    amount=0.40 + 0.08 * self. superposition,
                                    type=['followup'],
                                    uptime=self.uptime)
            
if __name__ == '__main__':
    from settings.BaseConfiguration import Configuration
    BeforeDawn(**Configuration).print()