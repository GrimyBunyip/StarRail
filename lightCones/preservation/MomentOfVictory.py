from baseClasses.BaseCharacter import BaseCharacter
from baseClasses.BaseLightCone import BaseLightCone
from baseClasses.BuffEffect import BuffEffect

class MomentOfVictory(BaseLightCone):
    def __init__(self,
                uptime:float=1.0,
                **config):
        self.loadConeStats('Moment of Victory')
        self.setSuperposition(config)
        self.uptime=uptime

    def equipTo(self, char:BaseCharacter):
        self.addStats(char)
        if char.path == self.path:
            char.addStat('Taunt',description=self.name,
                                        amount=2.0,
                                        mathType='percent')
            char.addStat('DEF',description=self.name,
                                    amount=0.2 + 0.04 * self.superposition,
                                    mathType='percent')
            char.addStat('DEF',description=self.name,
                                    amount=0.2 + 0.04 * self.superposition,
                                    mathType='percent',
                                    uptime=self.uptime)
            
if __name__ == '__main__':
    from settings.BaseConfiguration import Configuration
    MomentOfVictory(**Configuration).print()