from baseClasses.BaseCharacter import BaseCharacter
from baseClasses.BaseLightCone import BaseLightCone

class IndeliblePromise(BaseLightCone):
    def __init__(self,
                uptime:float = 1.0,
                superposition:int=None,
                **config):
        self.loadConeStats('Indelible Promise')
        self.setSuperposition(superposition,config)
        self.uptime = uptime
        self.nameAffix = f'{uptime:.2f} Uptime'

    def equipTo(self, char:BaseCharacter):
        self.addStats(char)
        if char.path == self.path:
            char.addStat('CR', description=self.name,
                        amount=0.1125 + 0.0375 * self.superposition)
            char.addStat('BreakEffect', description=self.name,
                        amount=0.21 + 0.07 * self.superposition,
                        uptime=self.uptime)
        
if __name__ == '__main__':
    from settings.BaseConfiguration import Configuration
    IndeliblePromise(**Configuration).print()