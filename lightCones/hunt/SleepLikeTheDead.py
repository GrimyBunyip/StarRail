from baseClasses.BaseCharacter import BaseCharacter
from baseClasses.BaseLightCone import BaseLightCone
from baseClasses.BuffEffect import BuffEffect

class SleepLikeTheDead(BaseLightCone):
    def __init__(self,
                uptime:float = 0.0,
                **config):
        self.loadConeStats('Sleep Like the Dead')
        self.setSuperposition(config)
        self.uptime = uptime

    def equipTo(self, char:BaseCharacter):
        self.addStats(char)
        if char.path == self.path:
            char.addStat('CD',description=self.name,
                                    amount=0.25 + 0.05 * self.superposition)
            char.addStat('CR',description=self.name,
                                    amount=0.30 + 0.06 * self.superposition,
                                    uptime=self.uptime)
        
if __name__ == '__main__':
    from settings.BaseConfiguration import Configuration
    SleepLikeTheDead(**Configuration).print()