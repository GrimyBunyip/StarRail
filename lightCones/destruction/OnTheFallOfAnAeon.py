from baseClasses.BaseCharacter import BaseCharacter
from baseClasses.BaseLightCone import BaseLightCone
from baseClasses.BuffEffect import BuffEffect

class OnTheFallOfAnAeon(BaseLightCone):
    def __init__(self,
                uptime:float = 0.25,
                stacks:float = 4.0,
                **config):
        self.loadConeStats('On the Fall of an Aeon')
        self.setSuperposition(config)
        self.uptime = uptime
        self.stacks = min(4.0,stacks)

    def equipTo(self, char:BaseCharacter):
        self.addStats(char)
        if char.path == self.path:
            char.addStat('ATK.percent',description=self.name,
                                    amount=0.06 + 0.02 * self.superposition,
                                    stacks=self.stacks)
            char.addStat('DMG',description=self.name,
                                    amount=0.09 + 0.03 * self.superposition,
                                    uptime=self.uptime)
        
if __name__ == '__main__':
    from settings.BaseConfiguration import Configuration
    OnTheFallOfAnAeon(**Configuration).print()