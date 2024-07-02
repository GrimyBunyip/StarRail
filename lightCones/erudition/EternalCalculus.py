from baseClasses.BaseCharacter import BaseCharacter
from baseClasses.BaseLightCone import BaseLightCone

class EternalCalculus(BaseLightCone):
    def __init__(self,
                uptimeAtk:float=1.0,
                uptimeSpd:float=1.0,
                superposition:int=None,
                **config):
        self.loadConeStats('Eternal Calculus')
        self.setSuperposition(superposition,config)
        self.uptimeAtk = uptimeAtk
        self.uptimeSpd = uptimeSpd

    def equipTo(self, char:BaseCharacter):
        self.addStats(char)
        if char.path == self.path:
            char.addStat('ATK.percent',description=self.name,
                                    amount=0.07 + 0.01 * self.superposition)
            char.addStat('ATK.percent',description=self.name,
                                    amount=0.03 + 0.01 * self.superposition,
                                    stacks=char.numEnemies,
                                    uptime=self.uptimeAtk)
            char.addStat('SPD.percent',description=self.name,
                                    amount=0.06 + 0.02 * self.superposition,
                                    uptime=self.uptimeSpd)
        
if __name__ == '__main__':
    from settings.BaseConfiguration import Configuration
    EternalCalculus(**Configuration).print()