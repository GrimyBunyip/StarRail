from baseClasses.BaseCharacter import BaseCharacter
from baseClasses.BaseCharacter import BaseCharacter
from baseClasses.BaseLightCone import BaseLightCone

class BaptismOfPureThought(BaseLightCone):
    def __init__(self,
                stacks:float = 3.0,
                uptime:float = 0.5,
                superposition:int=None,
                **config):
        self.loadConeStats('Baptism of Pure Thought', shortname='Baptism')
        self.setSuperposition(superposition,config)
        self.stacks = stacks
        self.uptime = uptime

    def equipTo(self, char:BaseCharacter):
        self.addStats(char)
        if char.path == self.path:
            char.addStat('CD',description=self.name,
                                    amount=0.17 + 0.03 * self.superposition)
            char.addStat('CD',description=self.name,
                                    amount=0.05 + 0.01 * self.superposition,
                                    stacks=self.stacks)
            char.addStat('DefShred',description=self.name,
                                    amount=0.20 + 0.04 * self.superposition,
                                    uptime=self.uptime,type=['followup'])
            char.addStat('DMG',description=self.name,
                                    amount=0.30 + 0.06 * self.superposition,
                                    uptime=self.uptime)
        
if __name__ == '__main__':
    from settings.BaseConfiguration import Configuration
    BaptismOfPureThought(**Configuration).print()