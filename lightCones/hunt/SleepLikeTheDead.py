from baseClasses.BaseCharacter import BaseCharacter
from baseClasses.BaseLightCone import BaseLightCone

class SleepLikeTheDead(BaseLightCone):
    def __init__(self,
                uptime:float = 0.0,
                superposition:int=None,
                **config):
        self.loadConeStats('Sleep Like the Dead')
        self.setSuperposition(superposition,config)
        self.uptime = uptime
        self.nameAffix = f'{uptime:.2f} Uptime'

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