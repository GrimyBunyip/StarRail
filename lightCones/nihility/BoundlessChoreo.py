from baseClasses.BaseCharacter import BaseCharacter
from baseClasses.BaseLightCone import BaseLightCone

class BoundlessChoreo(BaseLightCone):
    def __init__(self,
                uptime:float=1.0,
                superposition:int=None,
                **config):
        self.loadConeStats(name='Boundless Choreo')
        self.setSuperposition(superposition,config)
        self.uptime = uptime

    def equipTo(self, char:BaseCharacter):
        self.addStats(char)
        if char.path == self.path:
            char.addStat('CR',description=self.name,
                                    amount=0.06 + 0.02 * self.superposition)
            char.addStat('CD',description=self.name,
                                    amount=0.18 + 0.06 * self.superposition,
                                    uptime=self.uptime)

if __name__ == '__main__':
    from settings.BaseConfiguration import Configuration
    BoundlessChoreo(**Configuration).print()