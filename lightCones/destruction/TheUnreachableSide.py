from baseClasses.BaseCharacter import BaseCharacter
from baseClasses.BaseLightCone import BaseLightCone

class TheUnreachableSide(BaseLightCone):
    def __init__(self,
                uptime:float = 1.0,
                **config):
        self.loadConeStats('The Unreachable Side')
        self.setSuperposition(config)
        self.uptime = uptime
        self.nameAffix = f'{uptime:.2f} Uptime'

    def equipTo(self, char:BaseCharacter):
        self.addStats(char)
        if char.path == self.path:
            char.addStat('CR',description=self.name,
                                    amount=0.15 + 0.03 * self.superposition)
            char.addStat('HP.percent',description=self.name,
                                    amount=0.15 + 0.03 * self.superposition)
            char.addStat('DMG',description=self.name,
                                    amount=0.20 + 0.04 * self.superposition,
                                    uptime=self.uptime)
        
if __name__ == '__main__':
    from settings.BaseConfiguration import Configuration
    TheUnreachableSide(**Configuration).print()