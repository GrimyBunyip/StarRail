from baseClasses.BaseCharacter import BaseCharacter
from baseClasses.BaseLightCone import BaseLightCone

class UnderTheBlueSky(BaseLightCone):
    def __init__(self,
                uptime:float = 1.0,
                superposition:int=None,
                **config):
        self.loadConeStats('Under the Blue Sky')
        self.setSuperposition(superposition,config)
        self.uptime = uptime
        self.nameAffix = f'{uptime:.2f} Uptime'

    def equipTo(self, char:BaseCharacter):
        self.addStats(char)
        if char.path == self.path:
            char.addStat('CR',description=self.name,
                                    amount=0.09 + 0.03 * self.superposition,
                                    uptime=self.uptime)
            char.addStat('ATK.percent',description=self.name,
                                    amount=0.12 + 0.04 * self.superposition)
        
if __name__ == '__main__':
    from settings.BaseConfiguration import Configuration
    UnderTheBlueSky(**Configuration).print()