from baseClasses.BaseCharacter import BaseCharacter
from baseClasses.BaseLightCone import BaseLightCone
import math

class InTheNight(BaseLightCone):
    def __init__(self,
                superposition:int=None,
                speed:float=160.0,
                **config):
        self.loadConeStats('In the Night')
        self.setSuperposition(superposition,config)
        self.speed=speed

    def equipTo(self, char:BaseCharacter):
        self.addStats(char)
        if char.path == self.path:
            char.addStat('CR',description=self.name,
                                    amount=0.15 + 0.03 * self.superposition)
            
            num_stacks = math.floor( self.speed - 100.0 ) / 10.0
            num_stacks = min(num_stacks, 6)
            
            char.addStat('ATK.percent',description=self.name,
                                    amount=0.05 + 0.01 * self.superposition,
                                    stacks=num_stacks,
                                    type=['basic'])
            char.addStat('ATK.percent',description=self.name,
                                    amount=0.05 + 0.01 * self.superposition,
                                    stacks=num_stacks,
                                    type=['skill'])
            char.addStat('CD',description=self.name,
                                    amount=0.10 + 0.02 * self.superposition,
                                    stacks=num_stacks,
                                    type=['ultimate'])
        
if __name__ == '__main__':
    from settings.BaseConfiguration import Configuration
    InTheNight(**Configuration).print()