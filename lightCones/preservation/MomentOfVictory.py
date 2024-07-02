from baseClasses.BaseCharacter import BaseCharacter
from baseClasses.BaseLightCone import BaseLightCone

class MomentOfVictory(BaseLightCone):
    def __init__(self,
                uptime:float=1.0,
                superposition:int=None,
                **config):
        self.loadConeStats('Moment of Victory')
        self.setSuperposition(superposition,config)
        self.uptime=uptime

    def equipTo(self, char:BaseCharacter):
        self.addStats(char)
        if char.path == self.path:
            char.addStat('Taunt.percent',description=self.name,
                                        amount=2.0)
            char.addStat('DEF.percent',description=self.name,
                                    amount=0.2 + 0.04 * self.superposition)
            char.addStat('DEF.percent',description=self.name,
                                    amount=0.2 + 0.04 * self.superposition,
                                    uptime=self.uptime)
            
if __name__ == '__main__':
    from settings.BaseConfiguration import Configuration
    MomentOfVictory(**Configuration).print()