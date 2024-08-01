from baseClasses.BaseCharacter import BaseCharacter
from baseClasses.BaseLightCone import BaseLightCone

class OnTheFallOfAnAeon(BaseLightCone):
    def __init__(self,
                uptime:float = 0.5,
                stacks:float = 4.0,
                superposition:int=None,
                **config):
        self.loadConeStats('On the Fall of an Aeon',shortname='Aeon')
        self.setSuperposition(superposition,config)
        self.uptime = uptime
        self.stacks = min(4.0,stacks)
        self.nameAffix = f'{uptime:.2f} Uptime'

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