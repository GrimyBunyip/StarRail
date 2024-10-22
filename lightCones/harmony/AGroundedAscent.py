from baseClasses.BaseCharacter import BaseCharacter
from baseClasses.BaseLightCone import BaseLightCone

class AGroundedAscent(BaseLightCone):
    def __init__(self,
                superposition:int=None,
                **config):
        self.loadConeStats('A Grounded Ascent')
        self.setSuperposition(superposition,config)

    def equipTo(self, char:BaseCharacter):
        self.addStats(char)
        if char.path == self.path:
            char.addStat('BonusEnergyAttack',description=self.name,
                                    amount=0.055 + 0.005 * self.superposition,
                                    type=['skill','ultimate'])
            pass #harmony cones not yet implemented fully
            
if __name__ == '__main__':
    from settings.BaseConfiguration import Configuration
    AGroundedAscent(**Configuration).print()