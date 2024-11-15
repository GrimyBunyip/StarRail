from baseClasses.BaseCharacter import BaseCharacter
from baseClasses.BaseLightCone import BaseLightCone

class DreamsMontage(BaseLightCone):
    def __init__(self,
                superposition:int=None,
                bonusProcs:float=1.0,
                **config):
        self.bonusProcs = bonusProcs
        self.loadConeStats('Dreams\' Montage')
        self.setSuperposition(superposition,config)

    def equipTo(self, char:BaseCharacter):
        self.addStats(char)
        if char.path == self.path:
            char.addStat('SPD.percent', description=self.name,
                        amount=0.07 + 0.01 * self.superposition)
            char.addStat('BonusEnergyTurn', description='Dream Montage',
                         amount=2.5 + 0.5 * self.superposition, stacks=self.bonusProcs)
        
if __name__ == '__main__':
    from settings.BaseConfiguration import Configuration
    DreamsMontage(**Configuration).print()