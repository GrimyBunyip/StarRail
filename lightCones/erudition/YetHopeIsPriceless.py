from baseClasses.BaseCharacter import BaseCharacter
from baseClasses.BaseLightCone import BaseLightCone

class YetHopeIsPriceless(BaseLightCone):
    def __init__(self,
                cd:float=2.80,
                uptime:float=1.0,
                superposition:int=None,
                **config):
        self.loadConeStats('Yet Hope Is Priceless')
        self.setSuperposition(superposition,config)
        self.cd = cd
        self.uptime = uptime

    def equipTo(self, char:BaseCharacter):
        self.addStats(char)
        if char.path == self.path:
            char.addStat('CR',description=self.name,
                                    amount=0.13 + 0.03 * self.superposition)
            char.addStat('DMG',description=self.name,
                                    amount=0.10 + 0.02 * self.superposition,
                                    stacks=(self.cd - 1.2)/0.2,
                                    type=['followup'])
            char.addStat('DefShred',description=self.name,
                                    amount=0.16 + 0.04 * self.superposition,
                                    type=['followup','ultimate'])
        
if __name__ == '__main__':
    from settings.BaseConfiguration import Configuration
    YetHopeIsPriceless(**Configuration).print()