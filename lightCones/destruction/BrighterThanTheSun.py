from baseClasses.BaseCharacter import BaseCharacter
from baseClasses.BaseLightCone import BaseLightCone

class BrighterThanTheSun(BaseLightCone):
    def __init__(self,
                uptime:float = 1.0,
                stacks:float = 2.0,
                **config):
        self.loadConeStats('Brighter Than the Sun')
        self.setSuperposition(config)
        self.uptime = uptime
        self.stacks = stacks

    def equipTo(self, char:BaseCharacter):
        self.addStats(char)
        if char.path == self.path:
            char.addStat('CR',description=self.name,
                                    amount=0.15 + 0.03 * self.superposition)
            char.addStat('ATK.percent',description=self.name,
                                    amount=0.15 + 0.03 * self.superposition,
                                    stacks=self.stacks,
                                    uptime=self.uptime)
            char.addStat('ER',description=self.name,
                                    amount=0.05 + 0.01 * self.superposition,
                                    stacks=self.stacks,
                                    uptime=self.uptime)
        
if __name__ == '__main__':
    from settings.BaseConfiguration import Configuration
    BrighterThanTheSun(**Configuration).print()