from baseClasses.BaseCharacter import BaseCharacter
from baseClasses.BaseLightCone import BaseLightCone

class AfterTheCharmonyFall(BaseLightCone):
    def __init__(self,
                superposition:int=None,
                uptime:float=0.5,
                **config):
        self.loadConeStats('After the Charmony Fall', shortname='Charmony')
        self.setSuperposition(superposition,config)
        self.uptime = uptime

    def equipTo(self, char:BaseCharacter):
        self.addStats(char)
        if char.path == self.path:
            char.addStat('BreakEffect',description=self.name,
                         amount=0.21 + 0.07 * self.superposition,
                         uptime=self.uptime)
            char.addStat('SPD.percent',description=self.name,
                         amount=0.06 + 0.02 * self.superposition,
                         uptime=self.uptime)
            
if __name__ == '__main__':
    from settings.BaseConfiguration import Configuration
    AfterTheCharmonyFall(**Configuration).print()