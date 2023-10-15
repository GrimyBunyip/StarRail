from baseClasses.BaseCharacter import BaseCharacter
from baseClasses.BaseLightCone import BaseLightCone

class SolitaryHealing(BaseLightCone):
    def __init__(self,
                uptime:float=0.5,
                **config):
        self.loadConeStats('Solitary Healing')
        self.setSuperposition(config)
        self.uptime = uptime

    def equipTo(self, char:BaseCharacter):
        self.addStats(char)
        if char.path == self.path:
            char.addStat('BreakEffect',description=self.name,
                                        amount=0.15 + 0.05 * self.superposition)
            char.addStat('DMG',description=self.name,
                                    amount=0.18 + 0.06 * self.superposition,
                                    uptime=self.uptime,
                                    type=['dot'])
            # on kill energy not factored in
            
if __name__ == '__main__':
    from settings.BaseConfiguration import Configuration
    SolitaryHealing(**Configuration).print()